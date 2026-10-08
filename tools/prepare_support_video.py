"""Package approved local films for the static website without re-encoding.

Run with --source T:/JobApp/output/jobhub-support-video.
MP4 masters and editable presentation sources stay outside this repository.
"""
import argparse
import base64
import hashlib
import io
import json
import subprocess
import tarfile
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
REVISION = "20261008"
FILMS = {
    "ru": ("video-v18-a", "JobHub-Support-V18-Roger-1080p.mp4"),
    "en": ("video-v19-en", "JobHub-Support-English-1080p.mp4"),
    "pl": ("video-v20-pl", "JobHub-Support-Polish-1080p.mp4"),
    "uk": ("video-v21-uk", "JobHub-Support-Ukrainian-1080p.mp4"),
    "nl": ("video-v22-nl", "JobHub-Support-Dutch-1080p.mp4"),
}


def command(*args, cwd=None):
    return subprocess.run(args, check=True, capture_output=True, text=True, cwd=cwd).stdout


def install_hls():
    # Pinned, self-hosted Apache-2.0 library; no runtime third-party CDN.
    version = "1.7.3"
    with urlopen(f"https://registry.npmjs.org/hls.js/{version}") as response:
        metadata = json.load(response)
    with urlopen(metadata["dist"]["tarball"]) as response:
        package = response.read()
    expected = metadata["dist"]["integrity"].removeprefix("sha512-")
    assert base64.b64encode(hashlib.sha512(package).digest()).decode() == expected
    target = ROOT / "assets" / "vendor" / f"hls.js-{version}"
    target.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(package), mode="r:gz") as archive:
        for source, destination in (
            ("package/dist/hls.min.js", "hls.min.js"),
            ("package/LICENSE", "LICENSE"),
        ):
            (target / destination).write_bytes(archive.extractfile(source).read())
    (target / "SOURCE.txt").write_text(
        f"hls.js {version}\nhttps://github.com/video-dev/hls.js\n"
        f"{metadata['dist']['tarball']}\n{metadata['dist']['integrity']}\n"
        "Apache-2.0; distributed bundle unchanged.\n", encoding="utf-8"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    args = parser.parse_args()
    media_root = ROOT / "assets" / "support-video" / REVISION
    records = {}
    for language, (folder, name) in FILMS.items():
        source = args.source / folder / name
        target = media_root / language
        target.mkdir(parents=True, exist_ok=True)
        before = hashlib.sha256(source.read_bytes()).hexdigest()
        metadata = json.loads(command(
            "ffprobe", "-v", "error", "-show_entries", "format=duration,size",
            "-of", "json", str(source)
        ))["format"]
        # Fragmented MP4 retains the exact approved picture and AAC narration.
        command(
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
            "-map", "0:v:0", "-map", "0:a:0", "-c", "copy", "-f", "hls",
            "-hls_time", "6", "-hls_playlist_type", "vod", "-hls_segment_type", "fmp4",
            "-hls_flags", "independent_segments", "-hls_fmp4_init_filename", "init.mp4",
            "-hls_segment_filename", str(target / "segment-%03d.m4s"),
            str(target / "presentation.m3u8"), cwd=target
        )
        command(
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", "0.2",
            "-i", str(source), "-frames:v", "1", "-q:v", "3", str(target / "poster.jpg")
        )
        subtitle = args.source / folder / f"subtitles-{language}.srt"
        command(
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(subtitle),
            str(target / "subtitles.vtt")
        )
        files = list(target.iterdir())
        assert (target / "init.mp4").is_file()
        assert all(file.stat().st_size < 25 * 1024 * 1024 for file in files)
        assert hashlib.sha256(source.read_bytes()).hexdigest() == before
        records[language] = {
            "master": name,
            "master_sha256": before,
            "duration": float(metadata["duration"]),
            "bytes": sum(file.stat().st_size for file in files),
            "segments": len(list(target.glob("*.m4s"))),
            "largest_asset": max(file.stat().st_size for file in files),
            "video_audio_reencoded": False,
        }
        print(f"{language}: {records[language]['segments']} segments, {records[language]['duration']:.2f}s")
    (media_root / "manifest.json").write_text(
        json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    install_hls()


if __name__ == "__main__":
    main()
