from website import create_app

application = create_app()

if __name__ == "__main__":
    # application.run(debug=True, port=8000) 
    application.run(host="0.0.0.0")