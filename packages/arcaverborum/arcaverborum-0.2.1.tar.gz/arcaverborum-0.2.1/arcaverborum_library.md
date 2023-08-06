# Arca Verborum

Arca Verborum is a project to interface with the data from the GLED package.

The main available function is currently the one for performing weighted sampling of
languages based on their phylogenetic distance, on their geographic distance
accounting for areal effects
(currently computed as a simple Haversine distance between the coordinates),
and on the frequency among previous random samples.

When obtaining random samples for multiple iterations, it is strongly
recommended to obtain all the samples in a single pass, so that the
library can account for the potential oversampling of languages
belonging to outgroups.

Note that the loading of the distance matrices, particularly of the
geographic one, can take up to a minute on slower machines.

See code for more documentation, as below.

```python
>>> import arcaverborum
>>> sampler = arcaverborum.GLED_Sampler()
WARNING:root:Loading the phylogenetic matrix from GLED...
WARNING:root:Loading the geographic matrix from GLED...
WARNING:root:Rescaling the phylogenetic matrix...
WARNING:root:Rescaling the geographic matrix...
>>> for idx, langset in enumerate(sampler.sample(4, 10)):
...   print(idx, langset)
... 
0 ('TlamacazapaNahuatl_tlam1239', 'GaviaoDoJiparana_gavi1246', 'Tubar_tuba1279', 'Pei_peii1238')
1 ('IslandCarib_isla1278', 'Samburu_samb1315', 'Dahalo_daha1245', 'Potawatomi_pota1247')
2 ('VlaxRomani_vlax1238', 'Gwahatike_gwah1244', 'NezPerce_nezp1238', 'Kwakwala_kwak1269')
3 ('AnaTingaDogon_anat1248', 'Zulgo-Gemzek_zulg1242', 'SkoltSaami_skol1241', 'Xokleng_xokl1240')
4 ('Mangarrayi_mang1381', 'Narak_nara1264', 'Matses_mats1244', 'Ionic-AtticAncientGreek_anci1242')
5 ('Jeli_jeri1242', 'Burum-Mindik_buru1306', 'Kistane_kist1241', 'Bongo_bong1285')
6 ('Patwin_patw1250', 'WesternTamang_west2415', 'Kapori_kapo1250', 'Sakha_yaku1245')
7 ('Kuy_kuyy1240', 'Kistane_kist1241', 'Kuruaya_kuru1309', 'Bolivar-NorthChimborazoHighlandQuichua_chim1302')
8 ('Betaf_beta1253', 'Bargam_barg1252', 'Pengo_peng1244', 'Wuding-LuquanYi_wudi1238')
9 ('NuclearWintu_nucl1651', 'Munit_muni1257', 'Nyawaygi_nyaw1247', 'MadaCameroon_mada1293')
```
