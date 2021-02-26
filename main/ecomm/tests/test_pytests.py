
def test_get_index_view_status_code(client):
    response = client.get('/')
    assert response.status_code == 200


def test_get_goods_list_view_status_code(client, good):
    response = client.get('/goods/')
    assert response.status_code == 200
    assert bytes(str(good), encoding='utf-8') in response.content


def test_get_good_detail_view_status_code(client, good):
    response = client.get(f'/goods/{good.id}/')
    assert response.status_code == 200
    assert bytes(str(good), encoding='utf-8') in response.content


def test_add_good_by_seller_status_code(client, seller):
    client.force_login(seller.customuser.user)
    response = client.get('/goods/add/')
    assert response.status_code == 200


def test_edit_good_by_seller_status_code(client, seller, good):
    client.force_login(seller.customuser.user)
    response = client.get(f'/goods/{good.id}/edit/')
    assert response.status_code == 200


def test_add_good_by_user_with_permission_denied(client, user):
    client.force_login(user)
    response = client.get('/goods/add/')
    assert response.status_code == 403


def test_redirect_logout(client, good):
    response = client.get(f'/goods/{good.id}/edit/')
    assert response.status_code == 302
    assert response.url.startswith('/accounts/login/')

