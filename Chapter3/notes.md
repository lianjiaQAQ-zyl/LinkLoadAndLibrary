# 第三章 目标文件里有什么
## 3.1 目标文件的格式

1. ELF 文件格式：PIE 表示位置无关可执行文件。

| 类型     | ELF 类型标记  | 基本含义              |
| ------ | --------- | ----------------- |
| 可重定位文件 | `ET_REL`  | 供链接器进一步链接         |
| 可执行文件  | `ET_EXEC` | 可执行程序的一种文件类型      |
| 共享目标文件 | `ET_DYN`  | 共享库，也用于 PIE 可执行文件 |
| 核心转储文件 | `ET_CORE` | 保存进程状态，供调试分析      |
2. 使用 `file` 命令查看文件格式。

## 3.2 目标文件是什么样的

1. 目标文件将代码、数据等信息按照不同的属性，以 **节（section）** 的形式进行存储，有时候也叫做**段（segment）**。
2. 程序源代码编译后的机器指令经常放在 **代码段（Code Section）** 中，一般命名为 `.code` 或者 `.text` ，全局变量和局部静态变量数据经常放在 **数据段（Data Section）**，一般命名为 `.data`。
3. 未初始化的全局变量和局部静态变量放在 `.bss` 段，这是因为它们的默认值都是 0，放在 `.data` 段浪费空间。所以存放在 `.bss` 段中，利用 ELF 节头信息记录大小总和即可，相当于预留位置，并没有内容，也不在文件中占用空间。
4. 
   ```
		# 查看各节大小
		objdump -h elf_example.o
		
		# 查看变量属于哪个节
		objdump -t elf_example.o
		
		# 查看 .data 的实际字节
		objdump -s --section=.data elf_example.o
		
		# 尝试查看 .bss 的实际字节
		objdump -s --section=.bss elf_example.o
   ```

### 3.3 挖掘 SimpleSection.o

1. 利用交叉编译，生成 32 位 x86 平台 ELF 文件：
```bash
clang --target=i386-unknown-linux-gnu -c simplesection.c -o simplesection.o
```
2. 使用 `gnu objdump` 查看反汇编（llvm 的输出会有较大差别）：
   ![[simple.png]]
	- `CONTENTS ALLOC` 等内容表示各个段的属性，`CONTENTS` 表示这个段在文件中存在内容。

3. 根据 size 和位置可以绘制出文件结构：
   ![[file.png]]
4. 可以使用 `objcopy` 工具来将一个二进制文件作为目标文件中的一个段。
5. 可以使用 `__attribute__((section("FOO")))` 指定变量所处的段。

### 3.4 ELF 文件结构描述
