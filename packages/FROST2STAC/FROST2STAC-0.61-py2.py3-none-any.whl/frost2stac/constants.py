featureofinterest_id = "?$select=@iot.id&$expand=Datastreams($select=@iot.id;$top=1;$expand=Observations($top=1;$select=@iot.id))"
featureofinterest_id_empty = (
    "?$select=@iot.id&$expand=Observations($select=@iot.id;$top=1)"
)
phenomenonTime_string = (
    "?$select=@iot.id&$expand=Datastreams($select=@iot.id,phenomenonTime)"
)
epilon = 0.000001
