"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_acp.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow
#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#
def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    minutes = 0
    decreasing = control_dist_km
    TRIGGERS = [(200,200,34),(400,200,32),(600,200,30),(1000,400,28),(1300,300,26)]
    if brevet_dist_km < control_dist_km:
        control_dist_km = brevet_dist_km
    for trigger in TRIGGERS:
        km, l, max = trigger
        if control_dist_km > km:
            minutes += (l / max) * 60
        else:
            minutes += ((control_dist_km-(km-l))/max) * 60
            break
    rounded = round(minutes)
    return brevet_start_time.shift(minutes=rounded)


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    minutes = 0
    TRIGGERS = [(600,600,15),(1000,600,11.428),(1300,1000,13.333)]
    if brevet_dist_km < control_dist_km:
        control_dist_km = brevet_dist_km
    for trigger in TRIGGERS:
        km, l, max = trigger
        #print("km, max:", km, max)
        if control_dist_km > km:
            minutes += round((l / max) * 60)
        else:
            if control_dist_km <= 60: #oddity
                #print(control_dist_km, "is less than hard 60")
                #print("returning",control_dist_km,"/20 + 1H =",round((control_dist_km/20 + 1) *60))
                minutes += round((control_dist_km/20 + 1) *60)
                break
            elif control_dist_km <= 600:
                #print(control_dist_km, "is less than or equal to hard 600")
                #print("adding to minutes:",control_dist_km,"/ 15 = ",round((control_dist_km/15)) * 60)
                minutes += round((control_dist_km/15) * 60)
                break
            else:
                minutes += round(((control_dist_km - l) / max) * 60)
                break
    rounded = round(minutes)
    return brevet_start_time.shift(minutes=rounded)
