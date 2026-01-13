#from lsst.summit.utils import ConsDbClient
from lsst.daf.butler import Butler, CollectionType
import pandas as pd

COLLECTION_NAME = "LSSTCam/raw/DM-53155"

#with open("/sdf/home/y/yusra/.lsst/consdb.token", "r") as f:
    #token = f.read()
    #client = ConsDbClient(f"https://yusra:{token}@usdf-rsp.slac.stanford.edu/consdb")

#constraint = ("science_program = 'BLOCK-365' AND  "
              #" (s_ra >= 276 AND s_ra <= 324 AND s_dec >= -21 AND s_dec <= -14 AND band IN ('u','g','r', 'i', 'z', 'y'))")

#originalVisits = client.query(f" SELECT * from cdb_lsstcam.visit1 where {constraint}").to_pandas()
originalVisits = pd.read_csv('visits.csv')
print("visits:", len(originalVisits))

butler = Butler("/cephfs/grid/lsst/repos/dp2_prep", collections="LSSTCam/raw/all")
print(butler)

bad = pd.read_csv('bad.ecsv', comment="#")
print("Bad visits", len(bad))

WHERE= f"""instrument='LSSTCam' AND day_obs>={originalVisits.day_obs.min()} AND day_obs<={originalVisits.day_obs.max()}
        AND exposure.observation_type='science'
        AND (detector<189) and (detector NOT in (0, 20, 27, 65, 123, 161, 168, 188))
        """
# Removed:
# AND exposure.target_name IN ('{"', '".join(originalVisits.target_name.unique())}')

# The spatial constraints are ignored here. Must filter for the good visit
results = butler.registry.queryDatasets('raw', where=WHERE)
drefs = set([r for r in results])
print("All data refs", len(drefs))

visitSet = set(originalVisits["visit"])

print("visitSet ", len(visitSet))

# The spatial constraints are NOT reflected in drefs. Must select good visits selected from above
filteredRefs = [d for d in drefs if d.dataId["exposure"] in visitSet]
print("After filtering per query", len(filteredRefs))

# Remove bad visits
filteredRefs = [d for d in filteredRefs if d.dataId["exposure"] not in bad.exposure.values]
print("After filtering bad", len(filteredRefs))

# add to collection
butlerWrite = Butler("dp2_prep", writeable=True)
butlerWrite.collections.register(COLLECTION_NAME, CollectionType.TAGGED)
butlerWrite.registry.associate(COLLECTION_NAME, filteredRefs)

# DOUBLE CHECK EVERYTHING

results = butler.registry.queryDataIds(datasets="raw", collections=COLLECTION_NAME, dimensions=["visit"])
taggedVisits = set([r["visit"] for r in results])
print("total tagged visits", len(taggedVisits))

#exposure = client.query(f" SELECT visit_id, s_ra, s_dec, day_obs, target_name, band from cdb_lsstcam.visit1 where {constraint}").to_pandas()
#print("total in query", len(exposure))

print("visit IDs in tagged collection not in query: ", taggedVisits - set(originalVisits["visit"]))
diff = set(originalVisits["visit"]) - taggedVisits
diff2 = diff - set(bad.exposure.values)

print("n visit IDs in query not in tagged collection: ", len(diff2))
print("visit IDs in query not in tagged collection: ", diff2)
print("These visits are not in the tagged collection and were not excluded as bad: ")
print("They may not have had define visits run on them:")
# instrument,visit,band,day_obs,physical_filter
originalVisits[originalVisits["visit"].isin(diff2)][["visit", "day_obs", "band", "physical_filter"]]

