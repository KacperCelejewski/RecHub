
def test_test_page(client):
    response = client.get("/test/")
    assert response.status_code == 200
    assert b"Testing the Flask Application Factory Pattern" in response.data
