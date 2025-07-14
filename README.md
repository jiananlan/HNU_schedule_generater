# 欢迎使用 HNU（湖南大学） 教务系统导出课表转日历工具

项目地址：[https://github.com/jiananlan/HNU_schedule_generater](https://github.com/jiananlan/HNU_schedule_generater)

本项目用于将湖南大学教务系统导出的课表（xlsx 文件）一键转换为可导入手机日历的 `.ics` 文件，方便**在系统日历中查看课程安排、手机上课前即时提醒、系统日历小组件快速查询**。

## 使用指南

1. 登录湖南大学教务系统  
2. 点击“我的选课” → “课表查看” → “打印”导出课表为 `.xlsx` 文件  
3. 克隆本项目，并安装依赖：
```bash
   pip install holidays
   pip install openpyxl
```
4. 修改输入文件、本学期课程第一周的周一的日期（在代码中很好找出；许多与本项目类似功能的程序都需要，未来有可能通过一些算法实现省略）
5. 运行转换脚本：

```bash
   python A9.py
```
6. 建议将生成的 `.ics` 文件通过邮件发送到手机，导入日历（iPhone 推荐使用默认邮箱 App）

## 在线转换（开发中）

我正在开发网页版转换功能，计划通过 GitHub Pages + 云服务器实现免下载一键转换，当前预览版本见：
[https://jiananlan.github.io/HNU_schedule_generater/](https://jiananlan.github.io/HNU_schedule_generater/)

欢迎感兴趣的同学通过 GitHub Issue 联系我，一起完善项目！

---

本项目为学生自发、非盈利、基于兴趣开发，与湖南大学官方无关，仅希望为同学们提供便利。



