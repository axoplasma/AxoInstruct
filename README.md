# AxoInstruct
Multi-user cue lists and stage instructions with Ableton Live, ClyphX Pro and OSC
Create cue lists for live performances and send stage instructions to your mobile devices.

![](images/AxoInstruct_Social01.png)

![](images/AxoInstructOverview_02.jpg)

## Supports
* Multiple users/artists
* Mobile devices
* Extendible cue lists with any number of songs (acts), cues or artists
* Display of current cue and outlook on what's coming next

## Requires
* [Ableton Live](https://www.ableton.com/en/live/)
* [ClyphX Pro](https://isotonikstudios.com/product/clyphx-pro/) with [OSC User Actions (beta)](http://forum.nativekontrol.com/thread/3620/beta-osc-output-clyphx-pro)
* [Max4Live](https://www.ableton.com/en/live/max-for-live/) -- for midi note triggers (optional)
* [TouchOSC](https://hexler.net/products/touchosc) or comparable OSC-enabled software

## Setup
1. Download the OSC User Actions (beta) from the [ClyphX Pro forum](http://forum.nativekontrol.com/thread/3620/beta-osc-output-clyphx-pro) and copy them to the `user_actions` folder. If you have Live 10 on a Windows system, this will be `C:\ProgramData\Ableton\Live 10 Suite\Resources\MIDI Remote Scripts\ClyphX_Pro\clyphx_pro\user_actions`
2. Copy the file `AxoInstruct.py`from this repository to the `user_actions` folder. If you have Live 10 on a Windows system, this will be `C:\ProgramData\Ableton\Live 10 Suite\Resources\MIDI Remote Scripts\ClyphX_Pro\clyphx_pro\user_actions`
3. On your mobile device, have TouchOSC app installed and open the `AxoInstruct.touchosc` file on your device. More information on TouchOSC installation and template file transfer, refer to the [TouchOSC homepage](https://hexler.net/products/touchosc)
4. Find a folder for your cuelist XML file and remember the location. You will need the file path for setting up AxoInstruct in your Ableton Live set.
5. Edit the `Preferences.txt` of ClyphX Pro add settings for outgoing OSC communication:

```
#************************************* [OSC SETTINGS] **********************************
# This setting determines the OSC port number that ClyphX Pro will receive OSC messages from.
# The possible settings are any OSC port number.
INCOMING_OSC_PORT = 7005
OUTGOING_OSC_PORT = 7006
OSC_DEVICE_IP_ADDRESS = 192.168.0.255
```

Notes:
In this case, the broadcast address x.x.x.255 of a local network is used. This way, the OSC messages can be received by any device in the 192.168.0.x address range

## Usage
### Initialization
AxoInstructs needs to be initialized first. Usually. I usually have a setup scene in session view containing a clip called `[] init_instruct "c:/path/to/your/cuelist.xml"`. Specifying a file path allows you to use different cue lists for each Live set or even multiple cue list per Live set if needed.
If you omit the file path in the clip's name, AXOInstruct will use the script which is specified by default in `AxoInstruct.py`.
![](images/AxoInstructOverview_01.png)

### Switching between songs
Each XML cue list is capable of holding as many songs as you need. But there can always be only one song selected. The `prep` actions lets you switch between songs.
Since my Live sets are usually built around the session view, I have clips for that: e.g. `[] prep demo1` where "demo1" denotes a song's `song_id` from the XML cue list file:

```
<?xml version="1.0"?>
<collection>
    <song song_id="demo1" title="Demo Song 1">
```

The prep action parses the XML file and automatically displays the first cue for all categories (music/lighting/visuals). You don't have to manually select the first cue.

### Selecting cues
Example action: `[] instruct m 3` -- where "m" denotes the category music, "l" as in lighting and "v" as in visuals. "3" displays the third cue as well as the two subsequent cues. If you choose a number that is larger than the specified numbers of cues, the display will show `--`.


![](images/AxoInstructOverview_01.png)


## Different ways to use AxoInstruct
### Clips and/or Scenes in Session View
![](images/AxoInstructOverview_01.png)

### Locators in Arrangement View
![](images/AxoInstructArrangementLocators_01.png)

### Drum Racks with Max4Live Device for Midi Note Triggering
Ableton Drum Rack and the ClyphX Pro `Note Trigger Handler` Max4Live Ensemble
![](images/AxoInstructM4L_Rack_01.png)
![](images/AxoInstructM4L_Clip_01.png)
Note: The depicted M4L devices is not included in the demo `AxoInstructDemo.als`set since it's the intellectual property of NativeKontrol. Please use the M4L devices that comes along with your ClyphX Pro installation.
