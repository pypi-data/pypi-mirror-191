import os
import time
import wget
import shutil
import zipfile
import argparse
from pathlib import Path
from loguru import logger


class WindowsPackager:
    def create_package(self) -> None:
        args = self._parse_argv()
        self._download_love(love_version=args.love_version)
        self._download_game(group_name=args.group_name, project_name=args.project_name, commit_id=args.commit_id)
        self._create_game_love_archive(project_name=args.project_name, commit_id=args.commit_id)
        self._create_game_executable(project_name=args.project_name, love_version=args.love_version)
        self._create_game_final_archive(
            project_name=args.project_name,
            commit_id=args.commit_id,
            love_version=args.love_version,
        )
        if args.cleanup:
            self._cleanup(project_name=args.project_name, commit_id=args.commit_id, love_version=args.love_version)

    @staticmethod
    def _parse_argv() -> argparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-g",
            "--group-name",
            help="Specify Gitlab group name (e.g. stone-kingdoms)",
            type=str,
            required=True,
        )
        parser.add_argument(
            "-p",
            "--project-name",
            help="Specify Gitlab project name (e.g. stone-kingdoms)",
            type=str,
            required=True,
        )
        parser.add_argument(
            "-i",
            "--commit-id",
            default="master",
            help="Specify which commit id to checkout (e.g. master)",
            type=str,
            required=False,
        )
        parser.add_argument(
            "-l",
            "--love-version",
            default="11.4",
            help="Love version to package (e.g. 11.4)",
            type=str,
            required=False,
        )
        parser.add_argument(
            "-c",
            "--cleanup",
            action=argparse.BooleanOptionalAction,
            help="Cleanup intermediate directories and files",
        )
        return parser.parse_args()

    @staticmethod
    def build_gitlab_game_url(group_name: str, project_name: str, commit_id: str) -> str:
        source_code_archive_filename: str = f"{project_name}-{commit_id}.zip"
        return f"https://gitlab.com/{group_name}/{project_name}/-/archive/{commit_id}/{source_code_archive_filename}"

    @staticmethod
    def _build_game_filename(project_name: str, commit_id: str) -> str:
        return f"{project_name}-{commit_id}.zip"

    def _build_game_directory_name(self, project_name: str, commit_id: str) -> str:
        return Path(self._build_game_filename(project_name, commit_id)).stem

    @staticmethod
    def _build_game_archive_filename(project_name: str) -> str:
        return f"{project_name}.love"

    @staticmethod
    def _build_love_archive_filename(love_version: str) -> str:
        return f"love-{love_version}-win64.zip"

    @staticmethod
    def _build_love_directory(love_filename: str) -> str:
        return Path(love_filename).stem

    def _build_love_executable_path(self, love_version: str) -> Path:
        love_filename: str = self._build_love_archive_filename(love_version=love_version)
        love_directory: str = self._build_love_directory(love_filename=love_filename)
        return Path(love_directory, "love.exe")

    @staticmethod
    def _build_game_executable_filename(project_name: str) -> str:
        return f"{project_name}.exe"

    def _download_love(self, love_version: str) -> None:
        love_filename = self._build_love_archive_filename(love_version=love_version)
        love_directory = self._build_love_directory(love_filename=love_filename)
        love_url: str = f"https://github.com/love2d/love/releases/download/{love_version}/{love_filename}"
        if not os.path.exists(love_directory):
            if not os.path.exists(love_filename):
                logger.info(f"Downloading [{love_filename}] from [{love_url}]")
                wget.download(love_url, love_filename)
            logger.info(f"Extracting [{love_filename}]")
            shutil.unpack_archive(love_filename, ".")

    def _download_game(self, group_name: str, project_name: str, commit_id: str) -> None:
        game_filename: str = self._build_game_filename(project_name, commit_id)
        if not os.path.exists(Path(game_filename).stem):
            if not os.path.exists(game_filename):
                gitlab_game_url: str = self.build_gitlab_game_url(group_name, project_name, commit_id)
                logger.info(f"Downloading game [{game_filename}] from [{gitlab_game_url}]")
                wget.download(gitlab_game_url, game_filename)
            shutil.unpack_archive(game_filename, ".")

    def _create_game_love_archive(self, project_name: str, commit_id: str) -> None:
        """
        Create a love archive from game source code.
        """
        game_archive_filename = self._build_game_archive_filename(project_name)
        if not os.path.exists(game_archive_filename):
            logger.info(f"Creating game love archive [{game_archive_filename}]")
            directory = Path(self._build_game_directory_name(project_name, commit_id))
            with zipfile.ZipFile(game_archive_filename, mode="w") as archive:
                for file_path in directory.rglob("*"):
                    archive.write(file_path, arcname=file_path.relative_to(directory))

    def _create_game_executable(self, project_name: str, love_version: str) -> None:
        """
        Merge lua code and love executable into one executable.
        """
        love_executable_path = self._build_love_executable_path(love_version=love_version)
        game_executable_filename = f"{project_name}.exe"
        if not os.path.exists(game_executable_filename):
            logger.info(f"Creating game executable [{game_executable_filename}]")
            game_archive_filename = self._build_game_archive_filename(project_name)
            with open(game_archive_filename, "rb") as game_archive:
                with open(love_executable_path, "rb") as love_executable:
                    with open(game_executable_filename, "wb") as game_executable:
                        game_executable.write(love_executable.read())
                    with open(game_executable_filename, "ab") as game_executable:
                        game_executable.write(game_archive.read())

    def _create_game_final_archive(self, project_name: str, commit_id: str, love_version: str) -> None:
        """
        Love games require dynamic libraries (alongside love executable) to run properly.
        """
        game_directory_name: str = self._build_game_directory_name(project_name, commit_id)
        timestamp: str = time.strftime("%Y%m%d")
        game_final_archive_filename = f"{game_directory_name}-{timestamp}.zip"
        if not os.path.exists(game_final_archive_filename):
            logger.info(f"Creating game final archive [{game_final_archive_filename}]")
            with zipfile.ZipFile(game_final_archive_filename, mode="w") as archive:
                love_filename: str = self._build_love_archive_filename(love_version=love_version)
                love_directory: Path = Path(self._build_love_directory(love_filename=love_filename))
                for file_path in love_directory.rglob("*.dll"):
                    archive.write(file_path, arcname=file_path.relative_to(love_directory))
                game_executable_filename: str = self._build_game_executable_filename(project_name=project_name)
                archive.write(game_executable_filename)

    def _cleanup(self, project_name: str, commit_id: str, love_version: str) -> None:
        """
        Delete all intermediate files and directories
        """
        Path(self._build_game_filename(project_name=project_name, commit_id=commit_id)).unlink(missing_ok=True)
        shutil.rmtree(
            Path(self._build_game_directory_name(project_name=project_name, commit_id=commit_id)),
            ignore_errors=True,
        )
        love_archive_filename: str = self._build_love_archive_filename(love_version=love_version)
        shutil.rmtree(Path(self._build_love_directory(love_filename=love_archive_filename)), ignore_errors=True)
        Path(self._build_love_archive_filename(love_version=love_version)).unlink(missing_ok=True)
        Path(self._build_game_executable_filename(project_name=project_name)).unlink(missing_ok=True)
        Path(self._build_game_archive_filename(project_name)).unlink(missing_ok=True)
