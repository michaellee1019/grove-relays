### michaellee1019:grove
A Viam module that supports controlling Grove relays over I2C.

#### 4_channel_spdt_relay
This model implements support for the [Grove 4 Channel SPDT Relay](https://www.seeedstudio.com/Grove-4-Channel-SPDT-Relay-p-3119.html).

Example Config:
```
{
  "attributes": {},
  "depends_on": [],
  "model": "michaellee1019:grove:4_channel_spdt_relay",
  "name": "my-model",
  "type": "generic"
}
```

Example DoCommand:
```
{"pulse_one":{"address":"0x11", "bit":"0x2", "pulse_seconds": "1"}}
```