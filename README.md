# S012Cam website and manuals

Bilingual support and privacy pages for the S012Cam iPhone app.

Website: https://teyuan-lab.github.io/S012Cam-webpage-manual/

App Store: https://apps.apple.com/app/id6834323253

The site is static HTML/CSS/JavaScript, published by GitHub Pages from main at the repository root. No build service or external front-end dependencies are required.

English and Traditional Chinese manual sources are in `manuals/`. Published PDFs are in `assets/`. The camera reference uses the approved original iPhone 16 Pro screenshot with numbered document annotations.

To rebuild the manuals, run `python3 manuals/build_manuals.py` with ReportLab installed. The script uses macOS Arial Unicode and embeds its glyphs. It also writes the browser-readable HTML manuals. Update the font path when building on another operating system.

Contact: teyuan@gmail.com

Department of Optics and Photonics, National Central University, Taiwan.
