from setuptools import setup, find_packages ,find_namespace_packages          #这个包没有的可以pip一下

    
setup(
    name = "Sound_cls",      #这里是pip项目发布的名称
    version = "1.4.2",  #版本号，数值大的会优先被pip
    keywords = ("pip", "SICA","featureextraction"),
    description = "",
    license = "MIT Licence",
    long_description_content_type="text/markdown", 
    url = "https://gitee.com/yuanyunqaing",     #项目相关文件地址，一般是github
    author = "YuanYunQiang",
    author_email = "649756903@qq.com",
    include_package_data = True,
    platforms = "any",
    install_requires = ['torch',
                        'torchaudio',
                        'ffmpeg',
                        'resampy',
                        'soundfile',
                        'librosa',
                        'termcolor',
                        'pyaudio',
                        ] ,       
)
