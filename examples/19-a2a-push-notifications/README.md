# Example 19 — Native A2A Push Notifications

Demonstrates the official A2A push-notification capability: create/get/list/delete `TaskPushNotificationConfig` and actual callback delivery. SecureAgent only composes the SDK's `InMemoryPushNotificationConfigStore` and `BasePushNotificationSender`; it does not expose a Nebula push API.

```text
make init example-19
make run example-19 server
make run example-19 client
make clean example-19
```
