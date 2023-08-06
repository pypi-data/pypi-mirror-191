from setuptools import setup, find_packages ,find_namespace_packages       #这个包没有的可以pip一下

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(
    name = "mxpit",      #这里是pip项目发布的名称
    version = "1.4.4",  #版本号，数值大的会优先被pip
    keywords = ("pip", "SICA"),
    description = "Mxpi-train",
    license = "MIT Licence",
    long_description = long_description,
    long_description_content_type="text/markdown", 
    url = "https://github.com/yuanyunqiang/",     #项目相关文件地址，一般是github
    author = "YuanYunQiang",
    author_email = "649756903@qq.com",
    packages = find_namespace_packages(
                     include=["mxpit", "mxpit.*"], ),
    include_package_data = True,
    platforms = "any",
    install_requires = [
                        'numpy<1.24.0',
                        'onnx',
                        'onnx_simplifier',
                        'onnxruntime',
                        'onnxsim',
                        'opencv-python',
                        'mxpi-pycocotools',
                        'pycocotools',
                        'PyYAML',
                        'torchsummary',
                        'tqdm',
                        'pywin32',
                        'torch',
                        'torchvision',
                        'torchaudio',
                        'future',
                        'tensorboard',
                        'neural_compressor',
                        'ffmpeg',
                        'resampy',
                        'soundfile',
                        'librosa',
                        'termcolor',
                        'pyaudio'] ,        
)
