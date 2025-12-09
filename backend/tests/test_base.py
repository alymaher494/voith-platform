import pytest
from pathlib import Path
from src.downloader.base import BaseDownloader


class DummyDownloader(BaseDownloader):

    def validate_url(self, url):
        return True

    def download(self, url, **kwargs):
        return "test_path"


@pytest.fixture
def base_downloader(tmp_path):
    downloader = DummyDownloader(output_dir=str(tmp_path))
    yield downloader
    downloader.cleanup()


def test_base_init(base_downloader, tmp_path):
    assert base_downloader.output_dir == tmp_path
    assert base_downloader.output_dir.exists()
    assert base_downloader.pbar is None


def test_base_context_manager(base_downloader):
    with base_downloader as dl:
        assert dl == base_downloader
    assert base_downloader.pbar is None  # Cleaned up


def test_base_progress_hook(base_downloader, capsys):
    # Simulate downloading status
    base_downloader.progress_hook({
        "status": "downloading",
        "total_bytes": 1000,
        "downloaded_bytes": 500
    })
    captured = capsys.readouterr()
    assert "Downloading" in captured.err  # tqdm outputs to stderr

    # Simulate finished
    base_downloader.progress_hook({"status": "finished"})
    assert base_downloader.pbar is None


def test_base_abstract_methods():
    with pytest.raises(
            TypeError,
            match="Can't instantiate abstract class BaseDownloader"):
        BaseDownloader()
