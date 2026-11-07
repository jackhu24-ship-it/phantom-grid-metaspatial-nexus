import os, sys, math, json, asyncio, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont
import edge_tts

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEO_DIR = os.path.join(BASE_DIR, "05_DemoVideo_1440P")
OUTPUT_MP4 = os.path.join(VIDEO_DIR, "demo_video_1440p.mp4")
TEMP_DIR = os.path.join(VIDEO_DIR, "_temp_t06_build")
os.makedirs(TEMP_DIR, exist_ok=True)

W, H = 2560, 1440
FPS = 30

VOICE = "en-US-ChristopherNeural"

SCRIPT_DATA = [
    # Act 1
    {"act": 1, "title": "THE SPATIAL PRODUCTIVITY BOTTLENECK", "sub": "Traditional VR Controllers Fail Enterprise Workflows",
     "spoken": "Welcome to PHANToM Grid MetaSpatial Agentic Nexus, engineered for the Meta VR Start Developer Competition.",
     "telemetry": {"INPUT_MODE": "Optical 25-Joint", "LATENCY": "8.2 ms", "TRACK_A": "ASIL-D Idle", "VRAM": "12.4 GB / 50GB"}},
    {"act": 1, "title": "THE SPATIAL PRODUCTIVITY BOTTLENECK", "sub": "Traditional VR Controllers Fail Enterprise Workflows",
     "spoken": "Traditional productivity tools in virtual reality suffer from severe controller fatigue and flat window traps.",
     "telemetry": {"INPUT_MODE": "Optical 25-Joint", "LATENCY": "8.1 ms", "TRACK_A": "ASIL-D Running", "VRAM": "14.2 GB / 50GB"}},
    # Act 2
    {"act": 2, "title": "HANDS-FIRST WEBXR SPATIAL WORKBENCH", "sub": "Zero-Install Instant Launch Inside Meta Quest Browser",
     "spoken": "MetaSpatial Nexus introduces a hands-first spatial workbench running natively inside Meta Quest Browser.",
     "telemetry": {"INPUT_MODE": "Air Pinch & Poke", "LATENCY": "7.8 ms", "WEBXR_FPS": "90.0 FPS", "VRAM": "18.5 GB / 50GB"}},
    {"act": 2, "title": "HANDS-FIRST WEBXR SPATIAL WORKBENCH", "sub": "Zero-Install Instant Launch Inside Meta Quest Browser",
     "spoken": "Users command autonomous agent swarms through optical hand tracking, air pinches, and depth pokes.",
     "telemetry": {"INPUT_MODE": "Depth Poke Drag", "LATENCY": "7.5 ms", "WEBXR_FPS": "89.8 FPS", "VRAM": "21.1 GB / 50GB"}},
    # Act 3
    {"act": 3, "title": "REAL-TIME MULTI-AGENT DAG ORCHESTRATION", "sub": "Sub-Millisecond Shell State Machine Decoupled from Swarms",
     "spoken": "Our decoupled dual-track architecture pairs a deterministic shell state machine with a distributed agent swarm.",
     "telemetry": {"AGENTS_ACTIVE": "4 Swarm Nodes", "DAG_STATE": "Deterministic", "KINEMATIC_DAMP": "1.35x Active", "VRAM": "26.4 GB / 50GB"}},
    {"act": 3, "title": "REAL-TIME MULTI-AGENT DAG ORCHESTRATION", "sub": "Sub-Millisecond Shell State Machine Decoupled from Swarms",
     "spoken": "Planner, Executor, Sentry, and Purger nodes execute concurrently, providing live three-D manifold telemetry.",
     "telemetry": {"AGENTS_ACTIVE": "Planner+Executor", "DAG_STATE": "Concurrent", "KINEMATIC_DAMP": "1.35x Active", "VRAM": "29.8 GB / 50GB"}},
    # Act 4
    {"act": 4, "title": "PG-MOD-OMNI-HAND-01 EXTERNAL CONTROL", "sub": "Physical Control of Host OS, Blender, and CAD Tools",
     "spoken": "Through our sovereign omni-hand bridge, virtual gestures physically control host software via FastMCP.",
     "telemetry": {"OMNI_HAND": "L1~L4 Connected", "BLENDER_DOCK": "Active 60FPS", "FAST_MCP": "< 1.85us", "VRAM": "34.2 GB / 50GB"}},
    {"act": 4, "title": "PG-MOD-OMNI-HAND-01 EXTERNAL CONTROL", "sub": "Physical Control of Host OS, Blender, and CAD Tools",
     "spoken": "Air pinches dispatch zero-copy commands to Blender, CAD, and operating systems with zero manual typing.",
     "telemetry": {"OMNI_HAND": "Pinch Recognized", "CAD_STATUS": "Zero-Copy Link", "FAST_MCP": "< 1.85us", "VRAM": "36.8 GB / 50GB"}},
    # Act 5
    {"act": 5, "title": "ASIL-D 50GB GUARD & ZERO DATA RESIDUE", "sub": "Automotive Safety Integrity Level & Cryptographic Purging",
     "spoken": "Industrial safety is non-negotiable. Our ASIL-D sentry hardware-trips an emergency stop if memory reaches 50 gigabytes.",
     "telemetry": {"GUARD_STATE": "ASIL-D Armed", "ESTOP_THRESHOLD": "50.0 GB", "ZDR_PURGE": "Arming 2-Pass", "VRAM": "41.2 GB / 50GB"}},
    {"act": 5, "title": "ASIL-D 50GB GUARD & ZERO DATA RESIDUE", "sub": "Automotive Safety Integrity Level & Cryptographic Purging",
     "spoken": "Our two-pass bitwise purger guarantees exactly zero point zero zero megabytes of biometric residue upon completion.",
     "telemetry": {"GUARD_STATE": "Purge Fired", "ESTOP_THRESHOLD": "0xAA -> 0x00", "ZDR_PURGE": "0.00 MB Residual", "VRAM": "0.00 MB Wipe"}},
    # Act 6
    {"act": 6, "title": "6/6 INDUSTRIAL GATES VERIFIED", "sub": "Sovereign Tri-Standard Compliant Production Ready Release",
     "spoken": "With six out of six rigid industrial verification gates fully passed, MetaSpatial Nexus sets a new enterprise benchmark.",
     "telemetry": {"GATES_PASSED": "6/6 100% Green", "WORM_SEAL": "SHA-256 Valid", "RELEASE_TIER": "Production Ready", "VRAM": "Idle Stable"}},
    # Act 7: Official Closing (Rule 86)
    {"act": 7, "title": "OFFICIAL SOVEREIGN CLOSING", "sub": "PHANToM GRID Global Command & Solo Architect Mandate",
     "spoken": "This concludes our formal presentation for the Meta VR Start Developer Competition.",
     "telemetry": {"PRESENTATION": "Concluded", "COMMANDER": "Xiaomi", "ARCHITECT": "Jack Hu", "STATUS": "Official Close"}},
    {"act": 7, "title": "OFFICIAL SOVEREIGN CLOSING", "sub": "PHANToM GRID Global Command & Solo Architect Mandate",
     "spoken": "This project was architected and led by PHANToM GRID Leader Jack Hu, and produced by Commander Xiaomi. Thank you.",
     "telemetry": {"PRESENTATION": "Sealed", "COMMANDER": "Xiaomi", "ARCHITECT": "Jack Hu", "STATUS": "WORM Signed"}}
]

async def generate_speech_files():
    audio_meta = []
    for i, item in enumerate(SCRIPT_DATA):
        fn = os.path.join(TEMP_DIR, f"speech_{i:02d}.mp3")
        wav_fn = os.path.join(TEMP_DIR, f"speech_{i:02d}.wav")
        print(f"Generating TTS [{i+1}/{len(SCRIPT_DATA)}]...")
        comm = edge_tts.Communicate(item["spoken"], VOICE)
        await comm.save(fn)
        # Convert to WAV 48kHz stereo
        cmd = ["ffmpeg", "-y", "-i", fn, "-ar", "48000", "-ac", "2", wav_fn]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        # Probe duration
        probe = subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", wav_fn
        ]).decode().strip()
        dur = float(probe)
        audio_meta.append({"wav": wav_fn, "dur": dur, "data": item})
        print(f"Clip {i+1}: {dur:.2f}s")
    return audio_meta

def create_master_audio(audio_meta):
    concat_list = os.path.join(TEMP_DIR, "concat_speech.txt")
    with open(concat_list, "w", encoding="utf-8") as f:
        for m in audio_meta:
            clean_p = m["wav"].replace("\\", "/")
            f.write(f"file '{clean_p}'\n")
    
    raw_speech = os.path.join(TEMP_DIR, "speech_full.wav")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list, "-c", "copy", raw_speech],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    total_dur = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", raw_speech
    ]).decode().strip())
    
    ambient_wav = os.path.join(TEMP_DIR, "ambient_28db.wav")
    cmd_noise = [
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", f"anoisesrc=d={total_dur}:c=pink:r=48000:a=0.039",
        "-filter_complex", "volume=-28dB",
        ambient_wav
    ]
    subprocess.run(cmd_noise, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    master_audio = os.path.join(TEMP_DIR, "master_audio_mixed.wav")
    cmd_mix = [
        "ffmpeg", "-y",
        "-i", raw_speech,
        "-i", ambient_wav,
        "-filter_complex", "[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=2[aout]",
        "-map", "[aout]",
        master_audio
    ]
    subprocess.run(cmd_mix, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return master_audio, total_dur

def get_fonts():
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 46)
        font_sub = ImageFont.truetype("arial.ttf", 26)
        font_card_title = ImageFont.truetype("arialbd.ttf", 30)
        font_telemetry = ImageFont.truetype("consola.ttf", 22)
        font_badge = ImageFont.truetype("arialbd.ttf", 20)
        font_subtitle = ImageFont.truetype("arialbd.ttf", 36)
    except:
        font_title = font_sub = font_card_title = font_telemetry = font_badge = font_subtitle = ImageFont.load_default()
    return font_title, font_sub, font_card_title, font_telemetry, font_badge, font_subtitle

font_title, font_sub, font_card_title, font_telemetry, font_badge, font_subtitle = get_fonts()

def render_frame_06(act_idx, total_acts, title, subtitle_text, spoken_text, frame_i, total_frames, telemetry_data, pip_speaker="COMMANDER XIAOMI"):
    img = Image.new("RGB", (W, H), (9, 14, 26))
    draw = ImageDraw.Draw(img)
    t = frame_i / 30.0

    # 1. Background Grid & Space Mesh
    for x in range(0, W, 80):
        draw.line([(x, 0), (x, H)], fill=(16, 24, 40), width=1)
    for y in range(0, H, 80):
        draw.line([(0, y), (W, y)], fill=(16, 24, 40), width=1)

    # 2. Top Header & HUD Progress
    draw.rectangle([50, 35, W-50, 140], fill=(15, 23, 42), outline=(0, 229, 255), width=2)
    badge_text = f"ACT {act_idx}/{total_acts} :: META VR"
    draw.rectangle([70, 52, 380, 122], fill=(13, 148, 136), outline=(45, 212, 191), width=2)
    draw.text((90, 72), badge_text, fill=(255, 255, 255), font=font_card_title)
    draw.text((410, 52), title, fill=(255, 255, 255), font=font_title)
    draw.text((410, 104), subtitle_text, fill=(0, 229, 255), font=font_sub)

    # Progress bar
    prog = frame_i / max(1, total_frames)
    draw.rectangle([50, 140, 50 + int((W-100)*prog), 146], fill=(251, 191, 36))

    # 3. Left Spatial Viewport (62% width: 50 -> 1560)
    vx1, vy1, vx2, vy2 = 50, 165, 1560, 1250
    draw.rectangle([vx1, vy1, vx2, vy2], fill=(12, 19, 36), outline=(56, 189, 248), width=2)
    draw.rectangle([vx1, vy1, vx2, vy1+50], fill=(19, 30, 54))
    draw.text((vx1+25, vy1+12), "3D SPATIAL MANIFOLD & OPTICAL HAND TRACKING VIEWPORT", fill=(255, 255, 255), font=font_card_title)

    # Draw dynamic 3D contours / concentric ripples
    cx, cy = (vx1 + vx2)//2, (vy1 + vy2)//2 + 20
    for r in range(60, 480, 60):
        pulse_r = r + int(12 * math.sin(t * 3.0 + r))
        draw.ellipse([cx - pulse_r, cy - pulse_r * 0.55, cx + pulse_r, cy + pulse_r * 0.55], outline=(30, 58, 95), width=2)
    
    # Dynamic optical hand tracking rays
    hx, hy = cx + int(140 * math.cos(t * 1.5)), cy + int(70 * math.sin(t * 1.8))
    draw.line([(cx, cy), (hx, hy)], fill=(251, 191, 36), width=3)
    draw.ellipse([hx-14, hy-14, hx+14, hy+14], fill=(245, 158, 11), outline=(255, 255, 255), width=2)
    draw.text((hx+25, hy-10), "WebXR Joint Ray [Pinch]", fill=(251, 191, 36), font=font_badge)

    # 4. Right Telemetry Drawer (38% width: 1590 -> 2510)
    dx1, dy1, dx2, dy2 = 1590, 165, 2510, 830
    draw.rectangle([dx1, dy1, dx2, dy2], fill=(15, 23, 42), outline=(139, 92, 246), width=2)
    draw.rectangle([dx1, dy1, dx2, dy1+50], fill=(28, 25, 56))
    draw.text((dx1+25, dy1+12), "LIVE SENSOR & KINEMATIC TELEMETRY", fill=(255, 255, 255), font=font_card_title)

    ty = dy1 + 75
    for k, v in telemetry_data.items():
        draw.text((dx1+25, ty), f"[{k}]", fill=(167, 139, 250), font=font_telemetry)
        draw.text((dx1+300, ty), str(v), fill=(52, 211, 153), font=font_telemetry)
        ty += 40

    # 5. Lower-Right Live PIP Presenter Cam (1590 -> 2510, 855 -> 1250)
    px1, py1, px2, py2 = 1590, 855, 2510, 1250
    draw.rectangle([px1, py1, px2, py2], fill=(8, 12, 20), outline=(52, 211, 153), width=2)
    draw.rectangle([px1, py1, px2, py1+45], fill=(16, 40, 30))
    rec_pulse = (int(t * 2) % 2 == 0)
    draw.ellipse([px1+20, py1+14, px1+34, py1+28], fill=(239, 68, 68) if rec_pulse else (150, 30, 30))
    draw.text((px1+45, py1+10), f"LIVE CAM PIP // {pip_speaker}", fill=(255, 255, 255), font=font_badge)

    # Audio spectrum bar simulation
    for i in range(24):
        bx = px1 + 30 + i * 36
        bar_h = int(25 + 40 * abs(math.sin(t * 8.0 + i * 0.4)))
        draw.rectangle([bx, py2 - 35 - bar_h, bx + 22, py2 - 35], fill=(52, 211, 153))

    draw.text((px1+35, py1+70), "SPEECH LOCK: 0.00ms JITTER-FREE", fill=(156, 163, 175), font=font_badge)
    draw.text((px1+35, py1+105), "AUDIO SPECTRUM: EBU R128 (-28dB BED)", fill=(156, 163, 175), font=font_badge)

    # 6. Bottom Title Safe Subtitle Area (50 -> 2510, 1270 -> 1410)
    draw.rectangle([50, 1270, W-50, 1405], fill=(12, 18, 30), outline=(251, 191, 36), width=2)
    draw.rectangle([70, 1282, 340, 1320], fill=(217, 119, 6))
    draw.text((85, 1288), "PRESENTER VOICE", fill=(255, 255, 255), font=font_badge)

    words = spoken_text.split()
    lines = []
    curr = []
    for w in words:
        curr.append(w)
        if len(" ".join(curr)) > 85:
            lines.append(" ".join(curr))
            curr = []
    if curr:
        lines.append(" ".join(curr))

    sub_y = 1328
    for l in lines[:2]:
        draw.text((85, sub_y), l, fill=(255, 255, 255), font=font_subtitle)
        sub_y += 38

    return img

def main():
    print("=== STARTING META VR TEMPLATE-06 MASTER VIDEO PIPELINE ===")
    audio_meta = asyncio.run(generate_speech_files())
    master_audio, total_dur = create_master_audio(audio_meta)
    print(f"Master audio mixed. Duration: {total_dur:.2f}s")

    total_frames = int(total_dur * FPS)
    print(f"Rendering {total_frames} frames ({total_dur:.2f}s @ {FPS} FPS)...")

    # Start ffmpeg rawvideo pipe
    video_stream_mp4 = os.path.join(TEMP_DIR, "video_stream_1440p.mp4")
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{W}x{H}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        video_stream_mp4
    ]
    pipe = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    # Frame timeline scheduler
    current_frame = 0
    for m in audio_meta:
        clip_frames = int(m["dur"] * FPS)
        data = m["data"]
        act_num = data["act"]
        for f_in_clip in range(clip_frames):
            frame_img = render_frame_06(
                act_idx=act_num,
                total_acts=7,
                title=data["title"],
                subtitle_text=data["sub"],
                spoken_text=data["spoken"],
                frame_i=current_frame,
                total_frames=total_frames,
                telemetry_data=data["telemetry"],
                pip_speaker="COMMANDER XIAOMI"
            )
            pipe.stdin.write(frame_img.tobytes())
            current_frame += 1
            if current_frame % 300 == 0:
                print(f"Rendered {current_frame}/{total_frames} frames ({current_frame*100/total_frames:.1f}%)...")

    pipe.stdin.close()
    pipe.wait()
    print("Video frame generation completed.")

    # Mux audio and video
    print("Muxing final 1440P master MP4 with AAC 320k...")
    cmd_mux = [
        "ffmpeg", "-y",
        "-i", video_stream_mp4,
        "-i", master_audio,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "320k",
        OUTPUT_MP4
    ]
    subprocess.run(cmd_mux, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"Master Video Rendered: {OUTPUT_MP4}")
    print("=== TEMPLATE-06 META VR MASTER VIDEO COMPLETE ===")

if __name__ == "__main__":
    main()
