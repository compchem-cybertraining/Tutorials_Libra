mol load cube job1/Diag_992-WFN_04608_1-1_0.cube
display projection Orthographic
mol modstyle 0 0 CPK 1.000000 0.300000 12.000000 12.000000
display depthcue off
color Display Background white
axes location Off
mol color Name
mol representation CPK 1.000000 0.300000 12.000000 12.000000
mol selection all
mol material Opaque
mol addrep 0
mol modcolor 1 0 ColorID 0
mol modstyle 1 0 Isosurface 0.030000 0 0 0 1 1
mol color ColorID 0
mol representation Isosurface 0.030000 0 0 0 1 1
mol selection all
mol material Opaque
mol addrep 0
mol modcolor 2 0 ColorID 1
mol modstyle 2 0 Isosurface -0.030000 0 0 0 1 1
scale by 0.833000

render Tachyon Diag_992-WFN_04608_1-1_0 "/util/academic/vmd/1.9.2/lib/vmd/tachyon_LINUXAMD64 -aasamples 12 %s -format TGA -res 2048 2048 -o %s.tga"
