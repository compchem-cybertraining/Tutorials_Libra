mol load cube job1/Diag_992-WFN_04608_1-1_0.cube
display projection Orthographic
#mol modstyle 0 0 CPK 1.200000 0.300000 15.000000 12.000000
#mol representation CPK 1.200000 0.300000 15.000000 12.000000

mol delrep 0 0
mol color Name
mol representation Lines 1.000000
mol selection all
mol material Opaque
mol addrep 0
mol delrep 0 0
mol color ColorID 10
mol representation CPK 1.000000 0.300000 12.000000 12.000000
mol selection element Si
mol material Opaque
#EdgyShiny
mol addrep 0
mol color ColorID 10
mol representation CPK 1.000000 0.300000 12.000000 12.000000
mol selection element H
mol material Opaque
#EdgyShiny
mol addrep 0
mol modcolor 1 0 ColorID 8
mol color ColorID 8
mol representation CPK 1.000000 0.300000 12.000000 12.000000
mol selection element H Si
mol material Opaque
#EdgyShiny
mol addrep 0
mol modstyle 2 0 Lines 1.000000

mol addrep 0
mol modstyle 1 0 Isosurface 0.01 0 0 0 1 1
mol modmaterial 1 0 Opaque
mol modcolor 1 0 ColorID 0

mol addrep 0
mol modcolor 2 0 ColorID 1
mol modstyle 2 0 Isosurface -0.01 0 0 0 1 1

color Display Background white

display projection Orthographic
rotate y by 90.0



scale by 1.3
#color Element Si cyan
axes location off

render Tachyon Diag_992-WFN_04608_1-1_0 "/util/academic/vmd/1.9.2/lib/vmd/tachyon_LINUXAMD64 -aasamples 12 %s -format TGA -res 2048 2048 -o %s.tga"
