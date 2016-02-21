# art_check
check  the config of the game resource, especially art resource

The collect of the src art used in external has been ignored.

Start the tool with ./do_server.sh in Linux or do_client.bat in Windows.

模块说明：

do.py	    # 入口

config.py	# 配置

debug.py	# 调试信息打印

art.py		# 数据存储

evolve.py	# 多进程处理相关,multiprocessing

tool_xml.py	  # .xml处理相关，主要是利用xml.etree.ElementTree解析xml

tool_file.py	# 文件统计与读取等

art_src.py	  # 资源的原始引用，主要来自脚本或者csv配置，这部分直接用硬盘上的文件替代处理

art_chk.py	  # 资源检测，根据配置文件的相关规则检测每个类似xml文件的每一个tag配置

art_chain.py	# 形成引用关系链，eg:a->b->c, a->e, a->f, 表示a引用了b,e,f, b 引用了c
