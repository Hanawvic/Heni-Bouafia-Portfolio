from my_portfolio import create_app


app = create_app()

if __name__ == "__main__":
    create_app().run(host='localhost', port=5000, debug=True)