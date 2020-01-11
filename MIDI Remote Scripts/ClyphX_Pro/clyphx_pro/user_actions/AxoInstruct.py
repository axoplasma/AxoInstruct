from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase
import xml.etree.ElementTree as ET 
import os.path

class AxoInstruct(UserActionsBase):
    def create_actions(self):
        self.add_global_action('init_instruct', self.init_instruct)
        self.add_global_action('prep', self.prepare_song)
        self.add_global_action('instruct', self.instruct)
            
    def init_instruct(self, _, args):
        self.canonical_parent.show_message('file: %s' % file)
        if os.path.isfile(args[1:-1]):
            xmlfile = args[1:-1]
        else:
            xmlfile = 'c:/Users/audio/Documents/Axoplasma/INSTRUCT/instruct.xml'
        self.xmldata = ET.parse(xmlfile)
        self.canonical_parent.show_message('xml %s loaded' % xmlfile)
        self.canonical_parent.log_message('init_instruct: root is %s' % self.xmldata.getroot())
        self.textfields = ['title', 'now', 'n_now', 'next', 'n_next', 'later', 'n_later']
        self.categories = ['music', 'lighting', 'visuals']
        self.targets = {'music': 'm', 'lighting': 'm', 'visuals': 'j'}
        self._init_osc_display ()
        
    def prepare_song(self, _, args):
        root = self.xmldata.getroot()
        song_id = '%s' % args
        search_str = "./song/[@song_id='" + song_id + "']"
        self._generate_cuelists(search_str)
        self._send_title(search_str)
        self._send_cue('music', 0)
        self._send_cue('lighting', 0)
        self._send_cue('visuals', 0)
        
    def instruct(self, _, args):
        subargs = args.split()
        self.canonical_parent.show_message('subarg1: %s, subarg2: %s' % (subargs[0], subargs[1]))
        if int(subargs[1]) >= 0:
            if (subargs[0] == "m" or subargs[0] == "music"):
                category = 'music'
            elif (subargs[0] == "l" or subargs[0] == "lighting"):
                category = 'lighting'
            elif (subargs[0] == "v" or subargs[0] == "visuals"):
                category = 'visuals'
            self._send_cue(category, int(subargs[1]))
        
    def _init_osc_display(self):
        for category in self.categories:
            for fieldname in self.textfields:
                self.canonical_parent.clyphx_pro_component.trigger_action_list('OSC STR /%s/%s "--"' % (category, fieldname))
            self.canonical_parent.clyphx_pro_component.trigger_action_list('OSC FLT /%s/progress 0.0' % category)
            self.canonical_parent.show_message('init %s display complete' % category)

    def _generate_cuelists(self, search_str):
        root = self.xmldata.getroot()
        self.cuelists = []
        for category in self.categories:
            self.cuelists.append({'%s' % category: list(root.findall(search_str + "/instruction/[@category='%s']/target/[@target_id='%s']/cue" % (category, self.targets.get(category))))})
        self.canonical_parent.show_message('cuelist generation successful')
        
    def _send_title(self, search_str):
        root = self.xmldata.getroot()
        for song in root.findall(search_str):
            self.canonical_parent.show_message('song: %s %s' % (song.tag, song.attrib))
            for category in self.categories:
                self.canonical_parent.clyphx_pro_component.trigger_action_list('OSC STR /%s/title "%s"' % (category, song.attrib['title']))

    def _send_cue(self, category, cue_id):
        for x in self.cuelists:
            if x.get(category):
                cue = x.get(category)
        num = len(cue)
        if cue_id > 0:
            current_cue = cue_id - 1
        else:
            current_cue = cue_id
        if current_cue < num:
            self.canonical_parent.clyphx_pro_component.trigger_action_list('OSC STR /%s/now "%s"' % (category, cue[current_cue].text))
            self.canonical_parent.clyphx_pro_component.trigger_action_list('OSC STR /%s/n_now "%s"' % (category, current_cue+1))
            self.canonical_parent.clyphx_pro_component.trigger_action_list('OSC FLT /%s/progress 1.0' % (category))
        else:
            self.canonical_parent.clyphx_pro_component.trigger_action_list('OSC STR /%s/now "--"' % (category))
            self.canonical_parent.clyphx_pro_component.trigger_action_list('OSC STR /%s/n_now "--"' % (category))
            self.canonical_parent.clyphx_pro_component.trigger_action_list('OSC FLT /%s/progress 0.0' % (category))
        if current_cue + 1 < num:
            self.canonical_parent.clyphx_pro_component.trigger_action_list('OSC STR /%s/next "%s"' % (category, cue[current_cue+1].text))
            self.canonical_parent.clyphx_pro_component.trigger_action_list('OSC STR /%s/n_next "%s"' % (category, current_cue+2))
        else:
            self.canonical_parent.clyphx_pro_component.trigger_action_list('OSC STR /%s/next "--"' % (category))
            self.canonical_parent.clyphx_pro_component.trigger_action_list('OSC STR /%s/n_next "--"' % (category))
        if current_cue + 2 < num:
            self.canonical_parent.clyphx_pro_component.trigger_action_list('OSC STR /%s/later "%s"' % (category, cue[current_cue+2].text))
            self.canonical_parent.clyphx_pro_component.trigger_action_list('OSC STR /%s/n_later "%s"' % (category, current_cue+3))
        else:
            self.canonical_parent.clyphx_pro_component.trigger_action_list('OSC STR /%s/later "--"' % (category))
            self.canonical_parent.clyphx_pro_component.trigger_action_list('OSC STR /%s/n_later "--"' % (category))
        self.canonical_parent.log_message('cue/category: %s/%s' % (current_cue, category))
