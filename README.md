# Fundamentals of Radio Interferometry - 射电干涉基础

在SKA天文台公约签署后，中国加入SKA项目基本成为定局，中国迫切需要有更多的科学或工程人员参与这个人类历史上最伟大的天文望远镜的建设。但相对而言，射电干涉的相关技术与普通天文光学观测的概念差异甚远，特别是射电干涉成像与光学成像的概念区别非常大，这使得射电干涉的初学者觉得非常困难。

我一直想有一个机会，能把近几年团队的工作好好总结一下，编写一个相对简单易解的射电干涉阵的教程。在一个偶然的机会中在GitHUB上看到一个类似的项目，通读一遍后感觉很好，虽然还有很多章节没有完成，但基本结构已经成形。衷心向南非的团队祝贺，他们的工作让人敬佩，项目中的参与人员有些我很熟悉。我随后与项目负责人（Griffin Foster <griffin.foster@gmail.com>）发了邮件，说明有兴趣生成一个中文版本，很快得到了他的回信，说明他个人是没有问题的，但这个项目也已经有很长时间没有更新了。

本工作是一个基于Ipython notebook的射电干涉基础学习教材，也已经被NASSP选为硕士教材（https://ratt-ru.github.io/fundamentals_of_interferometry/)，力争通过社区的努力，通过持续改进和不断完善与更新，最终能成为一个射电干涉方面的基础教程，推进射电干涉阵技术能被更多的理解与解决。

为了共同的事业，欢迎有更多的人加入社团，加入本项目，一起贡献才智。为我国参与SKA项目能培养出更多的青年人才。

## 中文版本的说明
原有的英文版本客观地说仍存在很多不足，同时有很多章节还没有完成。中文版力争把这些内容重写，同时把后续没有完成的部分继续写完。此外，根据Python当前的发展趋势，中文版本将基于Python3版本。

如果项目可以结束，我们会争取把当前中文改进的部分再更新到英文版。

## 数据文件

为了运行与测试本项目，还需要一些额外的大数据文件 (> 1MB), 主要是FITS图像文件，请自行下载。 [here](https://www.dropbox.com/s/n3jyiajytwuldpu/fundamentals_fits.tar.gz?dl=0)), KAT-7仿真测量集（measurement sets）文件[here](https://www.dropbox.com/s/kb3p2mthei8dgl9/simulated_KAT-7_ms.tar.gz?dl=0)。文件均采用tar格式，需要在data子目录下解压使用.

```
cd fundamentals_of_interferometry/data/
tar xvzf fundamentals_fits.tar.gz
cd simulated_kat_7_vis
tar xvzf simulated_KAT-7_ms.tar.gz
```

## 版面风格说明（Style Guide）

为了保证内容的前后一致性，在本项目中采用了统一的风格，请后续维护与开发中保持这一风格 [style guide](https://github.com/griffinfoster/fundamentals_of_interferometry/blob/master/0_Introduction/0_introduction.ipynb)。此外，项目也给出了一个修订模板 [editing guide](https://github.com/griffinfoster/fundamentals_of_interferometry/blob/master/0_Introduction/editing_guide.ipynb) 供后续修订中参考使用。

## 设置VirtualENV (Setup contributor virtualenv)

如果您有意加入本项目，可以利用virtualenv构建同样的开发环境，以此保证您的软件环境与其它开发者一致。下面简单介绍如何在Ubuntu系统中(在14.04和16.04测试)设置相应的环境，如果是其它的环境需要有一些微小的修改。需要说明一下，在原项目中采用Python 2，但考虑到未来的发展，本项目修改了全部代码，全部移植到了Python3的环境。

目前建议使用pip来安装软件包，重要的软件包的版本需求如下:

* pip 7.1.2
* python 2.7.6P
* numpy 1.10.1
* matplotlib 1.5.0
* scipy 0.16.1
* ipython 4.2.0
* astropy 1.1.1
* aplpy 1.0
* ipywidgets 4.1.1
* healpy 1.10.3
* ephem 3.7.6.0

在开发中可以参考：

* <http://jeffskinnerbox.me/posts/2013/Oct/06/ipython-notebook-in-virtualenv/>
* <http://iamzed.com/2009/05/07/a-primer-on-virtualenv/>
* <http://jonathanchu.is/posts/virtualenv-and-pip-basics/>
* <https://warpedtimes.wordpress.com/2012/09/23/a-tutorial-on-virtualenv-to-isolate-python-installations/>

在安装虚拟环境前，根据不同系统的需要需要安装相应的一些底层库，如：

```
sudo apt-get install libpng-dev libncurses5-dev
```

设置一个可以运行本项目的干净环境，基本过程如下，先运行：:

```
$ which pip
```

如果没有报错，开始安装pip:

```
$ sudo easy_install pip
```

然后继续运行：

```
$ which virtualenv
```

如果没有报错，开始安装virtualenv:

```
$ sudo apt-get install python-virtualenv
$ sudo pip install virtualenvwrapper
```

如果系统中已经安装好了基础软件包，那就可以创新一个虚拟环境(virtualenv)，我个人倾向于在一个地方保存所有的虚拟环境，比如全部都放在一个目录下，或者都放在宿主目录(Home）下。

```
$ cd .virtualenv
$ virtualenv --no-site-packages fundamentals
```

上面这个命令就可以创新出一个基础的虚拟环境在.virtualenv目录下，这个目录与系统的site-packages是完全独立的，然后进一步激活这个虚拟环境：

```
$ cd fundamentals
$ source bin/activate
```

在基础环境完成后，先从github上克隆本仓库，克隆时可以从您fork后的项目中进行，这样会方便后面的更新：

```
$ git clone https://github.com/[username]/fundamentals_of_interferometry.git
```

如果只是希望运行本项目，那可以直接克隆本仓库.

```
$ git clone https://github.com/griffinfoster/fundamentals_of_interferometry.git
```

需要注意的是，更多初学者经常在这里迷糊，一定要记得在构建虚拟环境后，这个虚拟环境是一个完全干净的环境，也就是说在这个环境下没有安装什么软件包，根据软件的需要，我们需要自行安装不同的软件包。安装一般采用两种方法：1）根据项目需要手工运行pip逐个安装；2）直接利用需求文件（requirements file）来安装。一般推荐采用后者。当然如果在安装过程中出了错误，也也需要手工再来进行处理。一般来说，需求文件都放在主目录下[here](https://raw.githubusercontent.com/griffinfoster/fundamentals_of_interferometry/master/requirements.txt).

```
$ pip install --upgrade pip
$ pip install -r [path to file]/requirements.txt
```

或者：

```
$ pip install --upgrade pip
$ pip install yolk
$ pip install numpy
$ pip install matplotlib
$ pip install scipy
$ pip install ipython[all]
$ pip install --no-deps astropy
$ pip install aplpy
$ pip install healpy
$ pip install ipywidgets
$ pip install ephem
```

在上述安装都完成后，就可以开始运行ipython notebook服务器了:

```
$ cd fundamentals_of_interferometry
$ jupyter notebook
```

在运行后要停止服务，在终端窗口中按ctrl-c然后输入y即可。如果要解除virtualenv的激活状态，可以运行:

```
$ deactivate
```

如果在解除激活后又需要再次应用virtualenv，则可以在本项目的目录下运行:

```
$ source bin/activate
```

### Data

为了避免在项目中包含有大量的数据文件，为运行本项目，请自行下载所需要的数据集 [here](https://www.dropbox.com/s/n3jyiajytwuldpu/fundamentals_fits.tar.gz?dl=0), 还有一个仿真的KAT-7 measurement sets文件 [here](https://www.dropbox.com/s/kb3p2mthei8dgl9/simulated_KAT-7_ms.tar.gz?dl=0).

在本仓库的根目录下，找到data子目录 ``data/``，把下载好的数据文件在这个目录下解压，操作如下：

```
$ cd [fundamentals root]/data/
$ mv [location of download]/fundamentals_fits.tar.gz .
$ tar xvzf fundamentals_fits.tar.gz
$ cd simulated_kat_7_vis/
$ mv [location of download]/simulated_KAT-7_ms.tar.gz .
$ tar xvzf simulated_KAT-7_ms.tar.gz
```

#### freetype

If there is a freetype related error, try:

```
sudo apt-get install libfreetype6-dev
```

#### fortran

If there is a fortran related error, try:

```
sudo apt-get install gfortran
```

### 贡献人（Contributors）

感谢以下的项目原创人员：
* Alexander Akoto-Danso ([@akotodanso](https://github.com/akotodanso))
* Marcellin Atemkeng ([@atemkeng](https://github.com/atemkeng))
* Landman Bester ([@landmanbester](https://github.com/landmanbester))
* Tariq Blecher ([@TariqBlecher](https://github.com/TariqBlecher))
* Roger Deane ([@rdeane](https://github.com/rdeane))
* Griffin Foster ([@griffinfoster](https://github.com/griffinfoster))
* Marisa Geyer ([@marisageyer](https://github.com/marisageyer))
* Julien Girard ([@JulienNGirard](https://github.com/JulienNGirard))
* Trienko Grobler ([@Trienko](https://github.com/Trienko))
* Benna Hugo ([@bennahugo](https://github.com/bennahugo))
* Gyula (Josh) Jozsa ([@gigjozsa](https://github.com/gigjozsa))
* Ermias Abebe Kassaye ([@Ermiasabebe](https://github.com/Ermiasabebe))
* Jonathan Kenyon ([@JSKenyon](https://github.com/JSKenyon))
* Sphesihle Makhathini ([@SpheMakh](https://github.com/SpheMakh))
* Modhurita Mitra ([@modhurita](https://github.com/modhurita))
* Gijs Molenaar ([@gijzelaerr](https://github.com/gijzelaerr))
* Jared Norman ([@jfunction](https://github.com/jfunction))
* Ridhima Nunhokee ([@Chuneeta](https://github.com/Chuneeta))
* Simon Perkins ([@sjperkins](https://github.com/sjperkins))
* Laura Richter ([@LauraRichter](https://github.com/LauraRichter))
* Lerato Sebokolodi ([@Sebokolodi](https://github.com/Sebokolodi))
* Oleg Smirnov ([@o-smirnov](https://github.com/o-smirnov))
* Ulrich Mbou Sob ([@ulricharmel](https://github.com/ulricharmel))
* Tim Staley ([@timstaley](https://github.com/timstaley))
* Cyril Tasse ([@cyriltasse](https://github.com/cyriltasse))
* Kshitij Thorat ([@KshitijT](https://github.com/KshitijT))
* Etienne Bonnassieux ([@ebonnassieux](https://github.com/ebonnassieux))

针对后续版本与中文版本，主要有如下人员参与：
* Feng Wang([@cnwangfeng](https://github.com/cnwangfeng))
* Hui Deng ()
* Shoulin Wei()
* Ying Mei ()
