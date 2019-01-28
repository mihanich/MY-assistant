pactl set-default-sink alsa_output.platform-soc_audio.analog-stereo
aplay ../audio/Fb.wav
echo "If you heard sound - fix successfull. If not - try to find reason manually."
