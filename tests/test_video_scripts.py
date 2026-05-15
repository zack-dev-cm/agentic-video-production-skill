import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skill" / "agentic-video-production-publisher" / "scripts"


def run_script(name, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / name), *args],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )


class VideoProductionScriptsTest(unittest.TestCase):
    def test_checker_warns_when_shot_has_character_without_bible(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            final_video = root / "final.mp4"
            final_video.write_bytes(b"")
            bundle = root / "bundle.json"
            report = root / "qc.json"

            run_script(
                "init_video_bundle.py",
                "--out",
                str(bundle),
                "--title",
                "Character Bible Gap",
                "--runtime",
                "6",
                "--aspect-ratio",
                "16:9",
                "--final-video",
                str(final_video),
            )
            run_script(
                "add_video_shot.py",
                "--bundle",
                str(bundle),
                "--shot-id",
                "S001",
                "--runtime",
                "6",
                "--characters",
                "rose-pink-braids",
                "--prompt",
                "Audio: diegetic only - crowd roar and footsteps, no music.",
            )
            run_script("check_video_bundle.py", "--bundle", str(bundle), "--repo-root", str(root), "--out", str(report))

            payload = json.loads(report.read_text())
            messages = "\n".join(item["message"] for item in payload["warnings"])
            self.assertEqual(payload["status"], "REVIEW")
            self.assertIn("no character bible exists", messages)

    def test_checker_handles_bad_numeric_runtime(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bundle = root / "bundle.json"
            report = root / "qc.json"
            bundle.write_text(
                json.dumps(
                    {
                        "project": {"title": "Bad Runtime", "target_runtime_seconds": "not-a-number", "aspect_ratio": "16:9"},
                        "characters": [],
                        "music": {},
                        "shots": [{"shot_id": "S001", "runtime_seconds": "bad", "mode": "narrative", "prompt": ""}],
                        "assets": {},
                        "publish": {},
                    }
                )
            )

            run_script("check_video_bundle.py", "--bundle", str(bundle), "--repo-root", str(root), "--out", str(report))

            payload = json.loads(report.read_text())
            self.assertEqual(payload["status"], "BLOCK")
            self.assertTrue(any("must be numeric" in item["message"] for item in payload["errors"]))

    def test_youtube_and_tiktok_handoffs_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            final_video = root / "final.mp4"
            final_video.write_bytes(b"")
            bundle = root / "bundle.json"
            youtube = root / "youtube.json"
            tiktok = root / "tiktok.json"

            run_script(
                "init_video_bundle.py",
                "--out",
                str(bundle),
                "--title",
                "Publish Handoff",
                "--runtime",
                "6",
                "--aspect-ratio",
                "9:16",
                "--track-provider",
                "local",
                "--track-source",
                "local:test",
                "--rights-note",
                "Operator-owned test audio.",
                "--final-video",
                str(final_video),
            )
            run_script(
                "export_youtube_handoff.py",
                "--bundle",
                str(bundle),
                "--out",
                str(youtube),
                "--channel-name",
                "Test Channel",
                "--browser-profile",
                "yt-profile",
                "--video-title",
                "Publish Handoff",
                "--video-file",
                str(final_video),
            )
            run_script(
                "export_tiktok_handoff.py",
                "--bundle",
                str(bundle),
                "--out",
                str(tiktok),
                "--browser-profile",
                "tt-profile",
                "--video-file",
                str(final_video),
                "--caption",
                "Test caption",
                "--hashtag",
                "aivideo",
            )

            youtube_payload = json.loads(youtube.read_text())
            tiktok_payload = json.loads(tiktok.read_text())
            self.assertEqual(youtube_payload["run"]["browser_profile"], "yt-profile")
            self.assertEqual(tiktok_payload["platform"], "tiktok")
            self.assertEqual(tiktok_payload["content"]["hashtags"], ["#aivideo"])


if __name__ == "__main__":
    unittest.main()
