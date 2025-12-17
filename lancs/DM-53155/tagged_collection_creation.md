# Tagged collection creation at Lancs

A tagged collection is used to create a subset of visit images, based on the LSSTCam/raw collection, to be processed.

At USDF, Huan Lin used a series of these:

```yaml
inCollection: LSSTCam/raw/20250527-20250921/box_276_324_-21_-14/DM-52836,LSSTCam/raw/20250629-20250921/SV_DDF/DM-52836,LSSTCam/raw/SV_field/M49a/DM-52836,LSSTCam/raw/SV_field/COSMOS/DM-52836,LSSTCam/calib,LSSTCam/calib/unbounded,refcats,skymaps,pretrained_models,LSSTCam/calib/fgcmcal,LSSTCam/calib/DM-52145
```

whereas at IN2P3, Quentin Le Boulc'h and Gabriele Mainetti used a smaller subset:

```yaml
inCollection: LSSTCam/raw/DM-52894,LSSTCam/calib,LSSTCam/calib/unbounded,refcats,skymaps,pretrained_models,LSSTCam/calib/fgcmcal
```

i.e., only `LSSTCam/raw/DM-52894`
