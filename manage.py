from start import create_app

# 实例化create_app类
app = create_app()


if __name__ == '__main__':
    # app.run(port=8000, use_reloader=False)
    app.run(port=5000)
