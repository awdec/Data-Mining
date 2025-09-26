@echo off
echo ====================================================
echo Codeforces数据挖掘项目Windows快速启动
echo ====================================================

REM 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请确保Python已安装并在PATH中
    pause
    exit /b 1
)

REM 升级pip
echo 正在升级pip...
python -m pip install --upgrade pip

REM 安装核心依赖（避免编译问题）
echo 正在安装核心依赖...
python -m pip install Flask numpy matplotlib seaborn scikit-learn requests joblib --only-binary=all

REM 尝试安装pandas
echo 正在安装pandas...
python -m pip install pandas --only-binary=all
if errorlevel 1 (
    echo pandas安装失败，尝试安装较老版本...
    python -m pip install "pandas>=1.3.0,<2.0.0" --only-binary=all
)

echo ====================================================
echo 依赖安装完成，启动应用...
echo ====================================================

REM 检查数据文件
if not exist "codeforces_problems_with_solved.csv" (
    echo 数据文件不存在，正在获取...
    python api.py
)

REM 启动应用
echo 启动Web应用...
python app.py

pause