# DharmaEvent Protocol

`events.json` 是新加坡寺院全年法会日历入口。

- `temples` 保存寺院的稳定资料；寺院 `id` 一经发布不再修改。
- `events` 保存已经核实的法会，一个活动通过 `templeID` 关联寺院。
- 时间使用 ISO 8601，并统一采用 `Asia/Singapore` 时区。
- 每条法会应提供 `sourceURL` 与 `verifiedAt`，日期未确认时不要发布。
- 活动取消后保留记录，并将 `status` 改为 `cancelled`。

最小活动字段：`id`、`templeID`、`title`、`temple`、`start`、
`durationMinutes`、`address`、`icon`、`status`。可选字段为 `details`、
`signupURL`、`sourceURL`、`verifiedAt`。
