import os
import unittest
import pypdf

class TestMetaVRTournamentComplianceGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tourney_dir = os.path.dirname(os.path.abspath(__file__))

    def test_01_all_10_drawers_present(self):
        """Action 1: Verify all 10 standard engineering drawers exist."""
        required_drawers = [
            "01_Specs",
            "02_SourceCode",
            "03_CoverImage_16x9",
            "04_Slides_PDF",
            "05_DemoVideo_1440P",
            "06_LiveApp",
            "07_SubmissionPackage",
            "08_AuditReceipts",
            "09_ChaosReports",
            "10_Releases"
        ]
        for drawer in required_drawers:
            p = os.path.join(self.tourney_dir, drawer)
            self.assertTrue(os.path.exists(p), f"Required drawer {drawer} missing at {p}")

    def test_02_official_deck_pdf_exists(self):
        """Action 2: Official deck PDF must exist and be valid."""
        deck_dir = os.path.join(self.tourney_dir, "04_Slides_PDF")
        pdfs = [f for f in os.listdir(deck_dir) if f.endswith(".pdf")]
        self.assertTrue(len(pdfs) > 0, "No PDF found in 04_Slides_PDF")
        pdf_path = os.path.join(deck_dir, pdfs[0])
        reader = pypdf.PdfReader(pdf_path)
        self.assertEqual(len(reader.pages), 10, f"Deck must have 10 pages, found {len(reader.pages)}")

    def test_03_demo_video_1440p_exists(self):
        """Action 3: 1440P demo video MP4 must exist and be > 1MB."""
        mp4_p = os.path.join(self.tourney_dir, "05_DemoVideo_1440P", "demo_video_1440p.mp4")
        self.assertTrue(os.path.exists(mp4_p), f"demo_video_1440p.mp4 must exist at {mp4_p}")
        self.assertGreater(os.path.getsize(mp4_p), 1000000, "demo_video_1440p.mp4 must be > 1MB")

    def test_04_submission_package_ready(self):
        """Action 4: Submission package Markdown must exist."""
        sub_p = os.path.join(self.tourney_dir, "07_SubmissionPackage", "Devpost_Submission_Package.md")
        self.assertTrue(os.path.exists(sub_p), f"Submission copy missing at {sub_p}")

if __name__ == "__main__":
    unittest.main()
