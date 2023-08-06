# Renumics License Key

## To generate a new license key file

1. Generate an new unsigned license file for your features (e.g. spotlight and spotlight).
   All features will have the same expiration date, user, maximum version and empty value fields assigned.

```bash
PYTHONPATH=. scripts/generate_license_key.py renumics.key --user "markus maier" --expiration-date-iso "2021-01-01" --max-version 0.99 --feature spotlight --feature spotlight --is-test "no"
```

2. Check (and modify) your generated license file
   You can edit the particular fields of each individual feature now - if needed.

3. Sign your license file

```bash
PYTHONPATH=. scripts/sign_license_key.py renumics.key
```

The signed license file is stored in the default license archive folder /mnt/renumics-license-keys/
A signed license file can be modified and signed again.
