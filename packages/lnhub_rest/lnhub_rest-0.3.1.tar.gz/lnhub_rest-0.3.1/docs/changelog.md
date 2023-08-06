# Changelog

<!-- prettier-ignore -->
Name | PR | Developer | Date | Version
--- | --- | --- | --- | ---
✅ Test Supabase functions | [74](https://github.com/laminlabs/lnhub-rest/pull/74) | [fredericenard](https://github.com/fredericenard) | 2023-02-11 | 0.3.1
✅ Use static-testuser1 in tests | [84](https://github.com/laminlabs/lnhub-rest/pull/84) | [fredericenard](https://github.com/fredericenard) | 2023-02-10 |
🎨 Set public column in `init_instance` | [83](https://github.com/laminlabs/lnhub-rest/pull/83) | [falexwolf](https://github.com/falexwolf) | 2023-02-09 |
✅ Add test for instance validation | [82](https://github.com/laminlabs/lnhub-rest/pull/82) | [falexwolf](https://github.com/falexwolf) | 2023-02-09 | 0.3.0
🚸 Validate sqlite uniqueness for given `(storage, name)` | [81](https://github.com/laminlabs/lnhub-rest/pull/81) | [falexwolf](https://github.com/falexwolf) | 2023-02-09 |
🐛 Add error message return in `init_instance` | [79](https://github.com/laminlabs/lnhub-rest/pull/79) | [falexwolf](https://github.com/falexwolf) | 2023-02-09 |
✅ Update test to reflect changes in testuser2 owned instances | [78](https://github.com/laminlabs/lnhub-rest/pull/78) | [fredericenard](https://github.com/fredericenard) | 2023-02-09 |
🗃️ Unique constraint on db field | [75](https://github.com/laminlabs/lnhub-rest/pull/75) | [fredericenard](https://github.com/fredericenard) | 2023-02-08 |
🚚 Update migration file name | [76](https://github.com/laminlabs/lnhub-rest/pull/76) | [fredericenard](https://github.com/fredericenard) | 2023-02-08 |
🚸 Validate storage arg and db arg | [73](https://github.com/laminlabs/lnhub-rest/pull/73) | [falexwolf](https://github.com/falexwolf) | 2023-02-07 |
🍱 Add `hedera` schema module and improve schema validation | [72](https://github.com/laminlabs/lnhub-rest/pull/72) | [falexwolf](https://github.com/falexwolf) | 2023-02-07 |
🚚 Remove `_sbclient` suffix | [71](https://github.com/laminlabs/lnhub-rest/pull/71) | [falexwolf](https://github.com/falexwolf) | 2023-02-06 | 0.2.1
🐛 Delete account_instance entries before deleting an instance | [69](https://github.com/laminlabs/lnhub-rest/pull/69) | [fredericenard](https://github.com/fredericenard) | 2023-02-06 |
🎨 Replace ORM versions of init, load and add_storage with sbclient | [70](https://github.com/laminlabs/lnhub-rest/pull/70) | [falexwolf](https://github.com/falexwolf) | 2023-02-06 |
🐛 Fix ambiguous relationship | [67](https://github.com/laminlabs/lnhub-rest/pull/67) | [fredericenard](https://github.com/fredericenard) | 2023-02-06 |
🚑 Revert not nullable public on instance | [66](https://github.com/laminlabs/lnhub-rest/pull/66) | [falexwolf](https://github.com/falexwolf) | 2023-02-06 | 0.2.0
🗃️ Account instance foreign key | [65](https://github.com/laminlabs/lnhub-rest/pull/65) | [fredericenard](https://github.com/fredericenard) | 2023-02-06 |
✅ Update tests | [64](https://github.com/laminlabs/lnhub-rest/pull/64) | [fredericenard](https://github.com/fredericenard) | 2023-02-06 |
🗃️ Make public flag and permission field not nullable | [63](https://github.com/laminlabs/lnhub-rest/pull/63) | [fredericenard](https://github.com/fredericenard) | 2023-02-06 |
✅ Update tests | [62](https://github.com/laminlabs/lnhub-rest/pull/62) | [fredericenard](https://github.com/fredericenard) | 2023-02-06 |
🗃️ Create account_instance table and add columns to instance table | [61](https://github.com/laminlabs/lnhub-rest/pull/61) | [fredericenard](https://github.com/fredericenard) | 2023-02-06 |
✨ Retrieve account instances using join | [60](https://github.com/laminlabs/lnhub-rest/pull/60) | [fredericenard](https://github.com/fredericenard) | 2023-02-04 |
✨ Account instances endpoint | [59](https://github.com/laminlabs/lnhub-rest/pull/59) | [fredericenard](https://github.com/fredericenard) | 2023-02-04 |
✨ Enable to get account by handle | [58](https://github.com/laminlabs/lnhub-rest/pull/58) | [fredericenard](https://github.com/fredericenard) | 2023-01-31 |
✅ Update test account | [57](https://github.com/laminlabs/lnhub-rest/pull/57) | [fredericenard](https://github.com/fredericenard) | 2023-01-30 |
🗃️ Add image url field | [56](https://github.com/laminlabs/lnhub-rest/pull/56) | [fredericenard](https://github.com/fredericenard) | 2023-01-30 |
⚡ Generate public url for profile picture | [55](https://github.com/laminlabs/lnhub-rest/pull/55) | [fredericenard](https://github.com/fredericenard) | 2023-01-30 |
🥅 Raise exception if delete_ci_instances fails | [54](https://github.com/laminlabs/lnhub-rest/pull/54) | [fredericenard](https://github.com/fredericenard) | 2023-01-30 |
♻️ Separate Account and Profile | [53](https://github.com/laminlabs/lnhub-rest/pull/53) | [fredericenard](https://github.com/fredericenard) | 2023-01-29 |
♻️ Replace user profile by account | [52](https://github.com/laminlabs/lnhub-rest/pull/52) | [fredericenard](https://github.com/fredericenard) | 2023-01-29 |
👷 Clean users created by CI | [51](https://github.com/laminlabs/lnhub-rest/pull/51) | [fredericenard](https://github.com/fredericenard) | 2023-01-27 | 0.1.4
🔥 Drop auxuser table | [50](https://github.com/laminlabs/lnhub-rest/pull/50) | [fredericenard](https://github.com/fredericenard) | 2023-01-24 |
🔥 Drop auxuser table | [49](https://github.com/laminlabs/lnhub-rest/pull/49) | [fredericenard](https://github.com/fredericenard) | 2023-01-24 |
✅ Add auxiliary user table and add back migration tests | [47](https://github.com/laminlabs/lnhub-rest/pull/47) | [falexwolf](https://github.com/falexwolf) | 2023-01-23 |
🐛 Fix exception in `load_instance_sbclient`  | [45](https://github.com/laminlabs/lnhub-rest/pull/45) | [falexwolf](https://github.com/falexwolf) | 2023-01-20 | 0.1.3
✅ Test endpoints | [44](https://github.com/laminlabs/lnhub-rest/pull/44) | [fredericenard](https://github.com/fredericenard) | 2023-01-20 |
💚 Comment out test_model_definitions_match_ddl_postgres | [43](https://github.com/laminlabs/lnhub-rest/pull/43) | [fredericenard](https://github.com/fredericenard) | 2023-01-19 |
💚 Delete ci instances | [41](https://github.com/laminlabs/lnhub-rest/pull/41) | [fredericenard](https://github.com/fredericenard) | 2023-01-18 |
✨ Create delete_instance function | [40](https://github.com/laminlabs/lnhub-rest/pull/40) | [fredericenard](https://github.com/fredericenard) | 2023-01-16 |
✨ Create delete_instance_like function | [39](https://github.com/laminlabs/lnhub-rest/pull/39) | [fredericenard](https://github.com/fredericenard) | 2023-01-16 |
✅ Test get_profile function | [38](https://github.com/laminlabs/lnhub-rest/pull/38) | [fredericenard](https://github.com/fredericenard) | 2023-01-16 |
💄 Prettify sign up & log in logging | [37](https://github.com/laminlabs/lnhub-rest/pull/37) | [falexwolf](https://github.com/falexwolf) | 2023-01-16 |
🐛 Ensure to safely close connection with hub | [34](https://github.com/laminlabs/lnhub-rest/pull/34) | [fredericenard](https://github.com/fredericenard) | 2023-01-16 | 0.1.2
🐛 Fix import error in routers utils due to API change | [33](https://github.com/laminlabs/lnhub-rest/pull/33) | [fredericenard](https://github.com/fredericenard) | 2023-01-16 |
⬆️ Upgrade `lndb-setup` | [32](https://github.com/laminlabs/lnhub-rest/pull/32) | [falexwolf](https://github.com/falexwolf) | 2023-01-16 | 0.1.1
🚚 Move `_hub.py` from `lndb-setup` here, rename to `_sign_upin.py` | [31](https://github.com/laminlabs/lnhub-rest/pull/31) | [falexwolf](https://github.com/falexwolf) | 2023-01-16 | 0.1.0
🐛 Use account table | [30](https://github.com/laminlabs/lnhub-rest/pull/30) | [fredericenard](https://github.com/fredericenard) | 2023-01-15 |
🍱 Autogenerate ER diagram for each migration | [29](https://github.com/laminlabs/lnhub-rest/pull/29) | [falexwolf](https://github.com/falexwolf) | 2023-01-15 |
🏗️ Introduce `init_instance()`, refactor `Organization`, `Storage`, `Instance`, repurpose `Usermeta` to `Account` | [28](https://github.com/laminlabs/lnhub-rest/pull/28) | [falexwolf](https://github.com/falexwolf) | 2023-01-14 | 0.0.2
🚀 Deploy with cloud run | [27](https://github.com/laminlabs/lnhub-rest/pull/27) | [fredericenard](https://github.com/fredericenard) | 2023-01-14 |
🚚 Migrate hub to version 0.0.1 | [26](https://github.com/laminlabs/lnhub-rest/pull/26) | [falexwolf](https://github.com/falexwolf) | 2023-01-13 | 0.0.1
👷 Clean up CI config and add a migrations docs page | [25](https://github.com/laminlabs/lnhub-rest/pull/25) | [falexwolf](https://github.com/falexwolf) | 2023-01-13 |
📝 Clean up docs | [24](https://github.com/laminlabs/lnhub-rest/pull/24) | [falexwolf](https://github.com/falexwolf) | 2023-01-13 |
✅ Clean up tables in hub and start testing migrations | [23](https://github.com/laminlabs/lnhub-rest/pull/23) | [falexwolf](https://github.com/falexwolf) | 2023-01-13 |
🔨 Create deployment pipeline | [20](https://github.com/laminlabs/lnhub-rest/pull/20) | [fredericenard](https://github.com/fredericenard) | 2023-01-13 |
♻️ Simplify `Usermeta` | [22](https://github.com/laminlabs/lnhub-rest/pull/22) | [falexwolf](https://github.com/falexwolf) | 2023-01-13 |
➕ Add lndb-setup dependency | [21](https://github.com/laminlabs/lnhub-rest/pull/21) | [fredericenard](https://github.com/fredericenard) | 2023-01-13 |
♻️ Minimal backend | [19](https://github.com/laminlabs/lnhub-rest/pull/19) | [fredericenard](https://github.com/fredericenard) | 2023-01-13 |
🐛 Handle case where usermeta does not exists | [16](https://github.com/laminlabs/lnhub-rest/pull/16) | [fredericenard](https://github.com/fredericenard) | 2023-01-13 |
⬆️ Upgrade dependencies | [18](https://github.com/laminlabs/lnhub-rest/pull/18) | [fredericenard](https://github.com/fredericenard) | 2023-01-13 |
🔥 Comment out migration tests | [17](https://github.com/laminlabs/lnhub-rest/pull/17) | [fredericenard](https://github.com/fredericenard) | 2023-01-13 |
✅ Test migrations | [14](https://github.com/laminlabs/lnhub-rest/pull/14) | [falexwolf](https://github.com/falexwolf) | 2023-01-05 |
Remove lndb-rest dependency | [15](https://github.com/laminlabs/lnhub-rest/pull/15) | [fredericenard](https://github.com/fredericenard) | 2023-01-05 |
✨ Add migrations infra | [13](https://github.com/laminlabs/lnhub-rest/pull/13) | [falexwolf](https://github.com/falexwolf) | 2023-01-04 |
♻️ Move models into schema submodule | [12](https://github.com/laminlabs/lnhub-rest/pull/12) | [falexwolf](https://github.com/falexwolf) | 2023-01-04 |
✅ Check versions | [10](https://github.com/laminlabs/lnhub-rest/pull/10) | [fredericenard](https://github.com/fredericenard) | 2022-12-05 |
✅ Add unit tests for the two main endpoints | [9](https://github.com/laminlabs/lnhub-rest/pull/9) | [fredericenard](https://github.com/fredericenard) | 2022-12-05 |
Set up test environment | [8](https://github.com/laminlabs/lnhub-rest/pull/8) | [fredericenard](https://github.com/fredericenard) | 2022-12-05 |
Update run script | [6](https://github.com/laminlabs/lnhub-rest/pull/6) | [fredericenard](https://github.com/fredericenard) | 2022-12-01 |
🎨 Rename package | [4](https://github.com/laminlabs/lnhub-rest/pull/4) | [fredericenard](https://github.com/fredericenard) | 2022-11-30 |
Improve initialization scripts | [3](https://github.com/laminlabs/lnhub-rest/pull/3) | [fredericenard](https://github.com/fredericenard) | 2022-11-25 |
Create initialization scripts | [2](https://github.com/laminlabs/lnhub-rest/pull/2) | [fredericenard](https://github.com/fredericenard) | 2022-11-24 |
✨ Implement basic hub endpoints | [1](https://github.com/laminlabs/lnhub-rest/pull/1) | [fredericenard](https://github.com/fredericenard) | 2022-11-18 |
