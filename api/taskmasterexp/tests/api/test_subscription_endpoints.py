from taskmasterexp.database.managers import SubscriptionManager

ORDER_ID = "I-HBMDL8PL8571"


async def test_subscription_status(
    test_admin_client, test_admin_user, subscription_manager: SubscriptionManager
):
    response = test_admin_client.get("/subscriptions/status")
    assert response.status_code == 200
    assert response.json()["isActive"] == False

    await subscription_manager.add_subscription(test_admin_user.uuid, ORDER_ID)
    response = test_admin_client.get("/subscriptions/status")
    assert response.status_code == 200
    assert response.json()["isActive"] == False

    await subscription_manager.activate_subscription("I-HBMDL8PL8571", "plan_id")
    response = test_admin_client.get("/subscriptions/status")
    assert response.status_code == 200
    assert response.json()["isActive"] == True


async def test_activate_subscription(
    test_admin_client, subscription_manager: SubscriptionManager
):
    response = test_admin_client.post(
        "/subscriptions/activate", json={"orderId": ORDER_ID}
    )
    assert response.status_code == 200
    assert response.json()["isActive"] == False

    await subscription_manager.activate_subscription(ORDER_ID, "plan_id")

    response = test_admin_client.get("/subscriptions/status")
    assert response.status_code == 200
    assert response.json()["isActive"] == True


async def test_cancel_subscription(
    test_admin_client, test_admin_user, subscription_manager: SubscriptionManager
):
    await subscription_manager.add_subscription(test_admin_user.uuid, ORDER_ID)
    await subscription_manager.activate_subscription(ORDER_ID, "plan_id")

    response = test_admin_client.get("/subscriptions/status")
    assert response.status_code == 200
    assert response.json()["isActive"] == True

    response = test_admin_client.post("/subscriptions/cancel")
    assert response.status_code == 204

    response = test_admin_client.get("/subscriptions/status")
    assert response.status_code == 200
    assert response.json()["isActive"] == False