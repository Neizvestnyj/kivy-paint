# Simple paint app example

## Usage and installation
Download python [directly](https://www.python.org/downloads/) or use [conda environment](https://www.anaconda.com/products/distribution)

```shell
git clone https://github.com/Neizvestnyj/kivy-paint.git
cd kivy-paint
pip install -r requirements.txt
python main.py
```

### Build desktop application
```shell
pip install pyinstaller
pyinstaller main.spec -y
```

<img src="https://user-images.githubusercontent.com/40869738/218888677-6c3aace2-fcee-408d-8a7f-a0d8ad3c43a4.png" data-canonical-src="https://user-images.githubusercontent.com/40869738/218888677-6c3aace2-fcee-408d-8a7f-a0d8ad3c43a4.png" width="800" height="470" />


### Android
You can build an android application only on a **Unix** system.
To build *apk* and *aab* use [buildozer](https://github.com/kivy/buildozer) and [p4a](https://github.com/kivy/python-for-android)

```shell
pip install buildozer
```
<img src="https://user-images.githubusercontent.com/40869738/218889273-23be9498-91f1-4bfa-9dd7-464ae6bc402c.jpg" data-canonical-src="https://user-images.githubusercontent.com/40869738/218889273-23be9498-91f1-4bfa-9dd7-464ae6bc402c.jpg" width="200" height="400" />


```shell
buildozer android debug deploy run logcat
```

### iOS
To build iOS app use [kivy-ios](https://github.com/kivy/kivy-ios)

[kivy-ios installation](https://github.com/kivy/kivy-ios#installation--requirements)

```shell
toolchain build python3 kivy pillow plyer
toolchain pip install --no-deps kivymd
```
