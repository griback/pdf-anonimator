"""Build a versioned Windows executable without changing the original v3 binary."""
import hashlib
from pathlib import Path
import subprocess
import sys

from version import __version__


def main():
    if sys.platform != 'win32':
        raise SystemExit('Build the Windows executable on Windows.')
    root = Path(__file__).resolve().parent
    name = f'AnonimizadorPDF_v{__version__}'
    subprocess.run([
        sys.executable, '-m', 'PyInstaller', '--noconfirm', '--clean',
        '--onefile', '--windowed', '--name', name,
        '--specpath', str(root / 'build'),
        '--workpath', str(root / 'build' / name),
        '--distpath', str(root / 'dist'), str(root / 'anonimizador_pdf.py'),
    ], cwd=root, check=True)
    exe = root / 'dist' / (name + '.exe')
    checksum = hashlib.sha256(exe.read_bytes()).hexdigest()
    exe.with_suffix('.exe.sha256').write_text(f'{checksum}  {exe.name}\n', encoding='ascii')
    print(f'OK: {exe}')


if __name__ == '__main__':
    main()
