# Этот скрипт не работает. Вылетает и выдает битое видео (возможно по памяти,
# хотя ее у меня 64 ГБ).
ffmpeg -i ./files/effect_particles_80s.mp4 -filter_complex \
"[0:v]trim=0:80,setpts=PTS-STARTPTS[v0]; \
 [v0]split=8[v0_1][v0_2][v0_3][v0_4][v0_5][v0_6][v0_7][v0_8]; \
 [v0_1][v0_2]xfade=transition=fade:duration=1:offset=79[v1]; \
 [v1][v0_3]xfade=transition=fade:duration=1:offset=158[v2]; \
 [v2][v0_4]xfade=transition=fade:duration=1:offset=237[v3]; \
 [v3][v0_5]xfade=transition=fade:duration=1:offset=316[v4]; \
 [v4][v0_6]xfade=transition=fade:duration=1:offset=395[v5]; \
 [v5][v0_7]xfade=transition=fade:duration=1:offset=474[v6]; \
 [v6][v0_8]xfade=transition=fade:duration=1:offset=553[v7]; \
 [v7]trim=duration=600[final]" \
 -map "[final]" -c:v libx264 -pix_fmt yuv420p ./files/effect_particles_looped_600s.mp4 -y
