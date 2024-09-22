# Эта команда создает из 15-секундного видео другое видео длиной 80 секунд с нахлестом и фейдом

ffmpeg -i ./files/effect_particles.mp4 -filter_complex \
"[0:v]trim=0:15,setpts=PTS-STARTPTS[v0]; \
 [v0]split=6[v0_1][v0_2][v0_3][v0_4][v0_5][v0_6]; \
 [v0_1][v0_2]xfade=transition=fade:duration=1:offset=14[v1]; \
 [v1][v0_3]xfade=transition=fade:duration=1:offset=28[v2]; \
 [v2][v0_4]xfade=transition=fade:duration=1:offset=42[v3]; \
 [v3][v0_5]xfade=transition=fade:duration=1:offset=56[v4]; \
 [v4][v0_6]xfade=transition=fade:duration=1:offset=70[v5]; \
 [v5]trim=duration=80[final]" \
 -map "[final]" -c:v libx264 -pix_fmt yuv420p ./files/effect_particles_looped.mp4 -y
