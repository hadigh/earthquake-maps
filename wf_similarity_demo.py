import matplotlib.pyplot as plt
import matplotlib.patches as patches
from obspy import UTCDateTime
from obspy.clients.fdsn import Client
from matplotlib.ticker import ScalarFormatter

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
def process_wf(st, trim_starttime, trim_endtime, resample=None):
    if not st:
        return st
    pre_filt = [0.001, 0.005, 35, 50]
    st.remove_response(pre_filt=pre_filt)
    if resample:
        st.resample(resample)
    st.trim(starttime=trim_starttime, endtime=trim_endtime)
    return st

# Define event arrival times
p_arrival_eve1 = UTCDateTime("2018-05-09 07:58:25")
p_arrival_eve2 = UTCDateTime("2018-05-09 08:06:26.3")

# Fetch waveforms
st_au = get_wf("IRIS", "AU", "RABL", "BHZ", p_arrival_eve1 - 3 * 60, p_arrival_eve1 + 10 * 60)
st_am = get_wf("RASPISHAKE", "AM", "R67E0", "EHZ", p_arrival_eve1 - 3 * 60, p_arrival_eve1 + 10 * 60)

# Process & Trim Waveforms
st_au_trimmed1 = process_wf(st_au.copy(), p_arrival_eve1 - 2, p_arrival_eve1 + 120)
st_am_trimmed1 = process_wf(st_am.copy(), p_arrival_eve1 - 2, p_arrival_eve1 + 120)

st_au_trimmed2 = process_wf(st_au.copy(), p_arrival_eve2 - 2, p_arrival_eve2 + 120)
st_am_trimmed2 = process_wf(st_am.copy(), p_arrival_eve2 - 2, p_arrival_eve2 + 120)

# Create 3x1 figure
fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=False)

# Plot full AU waveform on top subplot
if st_au:
    time_full = st_am[0].times("relative")
    axes[0].plot(time_full, st_am[0].data, color='black', label="AU - RABL (BHZ)")
    axes[0].set_title("Original RS Waveform with Event Windows")
    axes[0].set_ylabel("Amplitude (counts)")
    

    # Highlight event windows
    event1_start = (p_arrival_eve1 - 2) - (p_arrival_eve1 - 3 * 60)
    event1_width = (p_arrival_eve1 + 120) - (p_arrival_eve1 - 2)
    
    event2_start = (p_arrival_eve2 - 2) - (p_arrival_eve1 - 3 * 60)
    event2_width = (p_arrival_eve2 + 120) - (p_arrival_eve2 - 2)

    ylim = axes[0].get_ylim()
    box_height = ylim[1] - ylim[0]

    rect1 = patches.Rectangle((event1_start, ylim[0]), event1_width, box_height, linewidth=2, edgecolor='red', facecolor='none', label="Event 1")
    rect2 = patches.Rectangle((event2_start, ylim[0]), event2_width, box_height, linewidth=2, edgecolor='blue', facecolor='none', label="Event 2")

    axes[0].add_patch(rect1)
    axes[0].add_patch(rect2)
    axes[0].legend()
    axes[0].set_xticklabels([])
    axes[0].yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    axes[0].ticklabel_format(style='sci', axis='y', scilimits=(0,0))

# Plot trimmed waveforms for Event 1 (AU and AM)
if st_au_trimmed1 and st_am_trimmed1:
    axes[1].plot(st_au_trimmed1[0].times("relative"), st_au_trimmed1[0].data, color='red', label="AU - RABL (BHZ)")
    axes[1].plot(st_am_trimmed1[0].times("relative"), st_am_trimmed1[0].data, color='blue', label="RS - R67E0 (EHZ)", linestyle="dashed")
    axes[1].set_title(f"Trimmed Waveform Comparison (Event 1: {p_arrival_eve1})")
    axes[1].set_ylabel("Amplitude (m/s)")
    axes[1].legend()
    axes[1].set_xticklabels([])
    axes[1].yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    axes[1].ticklabel_format(style='sci', axis='y', scilimits=(0,0))

# Plot trimmed waveforms for Event 2 (AU and AM)
if st_au_trimmed2 and st_am_trimmed2:
    axes[2].plot(st_au_trimmed2[0].times("relative"), st_au_trimmed2[0].data, color='red', label="AU - RABL (BHZ)")
    axes[2].plot(st_am_trimmed2[0].times("relative"), st_am_trimmed2[0].data, color='blue', label="RS - R67E0 (EHZ)", linestyle="dashed")
    axes[2].set_title(f"Trimmed Waveform Comparison (Event 2: {p_arrival_eve2})")
    axes[2].set_xlabel("Time (s)")
    axes[2].set_ylabel("Amplitude (m/s)")
    axes[2].legend()
    axes[2].set_xlim(0,120)
    axes[2].set_xticklabels([])
    axes[2].yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    axes[2].ticklabel_format(style='sci', axis='y', scilimits=(0,0))

# Adjust layout and show plot
plt.tight_layout()

plt.savefig("../outputs/waveform_similarity.png", dpi=600, bbox_inches="tight")
plt.show()
