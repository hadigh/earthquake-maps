import matplotlib.pyplot as plt
from obspy import UTCDateTime
from obspy.clients.fdsn import Client
import pandas as pd


# Function to fetch waveform
def get_wf(client_id, network, station, channel, starttime, endtime):
    client = Client(client_id)
    try:
        st = client.get_waveforms(
            network=network,
            station=station,
            channel=channel,
            starttime=starttime, 
            endtime=endtime,
            location="*",
            attach_response=True
        )
    except Exception as e:
        print(f"Error fetching {network} {station}: {e}")
        st = []
    return st

# Function to process waveform (remove response, trim, resample)
def process_wf(st, fhpc=0.1, flpc=25):
    if not st:
        return st
    st.detrend()
    pre_filt = [0.005, 0.01, 35, 50]
    st.remove_response(pre_filt=pre_filt)
    st.filter("bandpass", freqmin=fhpc, freqmax=flpc, zerophase=True)
    st.detrend('linear')
    st.detrend('demean')
    st.trim(starttime= st[0].stats.starttime + 30, endtime=st[0].stats.endtime - 60)
    st.detrend('linear')
    st.detrend('demean')
    return st

def get_station_coords(client_id, network, station, starttime, endtime):
    client = Client(client_id)
    inv = client.get_stations(network=network,station=station,starttime=starttime, endtime=endtime)
    sta_lat = inv[0][0].latitude
    sta_lon = inv[0][0].longitude
    return sta_lat, sta_lon

# Define event arrival times
ot_eve1 = UTCDateTime("2025-02-22 14:16:16")- 1*60
ot_eve2 = UTCDateTime("2025-02-23 01:24:23")- 1*60

# # Fetch waveforms
# st1_eve1 = get_wf("RASPISHAKE", "AM", "R9928", "EHZ", ot_eve1, ot_eve1 + 5 * 60)
# st2_eve1 = get_wf("RASPISHAKE", "AM", "R1458", "EHZ", ot_eve1, ot_eve1 + 5* 60)

# st1_eve2 = get_wf("RASPISHAKE", "AM", "R9928", "EHZ", ot_eve2, ot_eve2 + 5 * 60)
# st2_eve2 = get_wf("RASPISHAKE", "AM", "R1458", "EHZ", ot_eve2, ot_eve2 + 5 * 60)

# # Process & Trim Waveforms
# st1_eve1_processed = process_wf(st1_eve1.copy())
# st2_eve1_processed = process_wf(st2_eve1.copy())

# st1_eve2_processed = process_wf(st1_eve2.copy())
# st2_eve2_processed = process_wf(st2_eve2.copy())

# #
# df = pd.DataFrame()
# df["time"] = st1_eve1_processed[0].times("relative")
# df["event1_station1"] = st1_eve1_processed[0].data
# df["event1_station2"] = st2_eve1_processed[0].data
# df["event2_station1"] = st1_eve2_processed[0].data
# df["event2_station2"] = st2_eve2_processed[0].data

# df.to_csv("timeseries.csv")


# table
sta1_lat, sta1_lon = get_station_coords("RASPISHAKE", "AM", "R9928", ot_eve2, ot_eve2 + 1 )
print(sta1_lat)
print(sta1_lon)

sta2_lat, sta2_lon = get_station_coords("RASPISHAKE", "AM", "R1458", ot_eve2, ot_eve2 + 1 )
print(sta2_lat)
print(sta2_lon)

# # Create 3x1 figure
# fig, axes = plt.subplots(2, 2, figsize=(10, 10), sharex=False)

# # Plot full AU waveform on top subplot
# time_full = st1_eve1_processed[0].times("relative")
# axes[0,0].plot(time_full, st1_eve1_processed[0].data, color='black', label="st1-eve1")
# axes[0,0].set_ylabel("Velocity (m/s)")

# axes[1,0].plot(time_full, st2_eve1_processed[0].data, color='black', label="st2-eve1")
# axes[1,0].set_ylabel("Velocity (m/s)")

# axes[0,1].plot(time_full, st1_eve2_processed[0].data, color='black', label="st1-eve2")
# axes[0,1].set_ylabel("Velocity (m/s)")

# axes[1,1].plot(time_full, st2_eve2_processed[0].data, color='black', label="st2-eve2")
# axes[1,1].set_ylabel("Velocity (m/s)")



# plt.show()