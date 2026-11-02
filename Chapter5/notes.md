## 第五章 Windows PE/COFF

### 5.1 Windows 的二进制文件格式 PE/COFF
1. PE(Protable Executable) 文件格式也是由 COFF（Common Object File Format）格式发展而来。
2. 在 `PE/COFF` 文件中，代码段往往命名为 `.code`，数据段命名为 `.data`

### 5.2 PE的前身——COFF
1. Microsoft Visual C++ 编译环境：
	- 编译器：cl（compile），将 `.c` 编译为 `.obj`，再调用链接器生成 `.exe`。
	- 链接器：link
	- 可执行文件查看器：dumpbin
2. `.drectve` 段是编译器传递给链接器的指令，即编译器希望告诉链接器如何来链接这个文件。
3. 符号表类型：
	- ABS（absolute）：表示符号是个绝对值，即一个常量，不存在任何段中
	- SECT1（section #1)：表示符号位于 COFF 文件的第一个段中。
	- UNDEF（Undefined）：表示符号在其他目标文件中

