"""Provides a list of randomly-generated texts by https://hipsum.co/"""

import random

class JglTexts():
    def __init__(self) -> None:
        """Loads in text bank from Hipster Ipsum"""
        
        self.possible_texts = {1: "I'm baby synth fixie 3 wolf moon green juice kinfolk pour-over crucifix vinyl jianbing craft beer celiac kickstarter church-key four loko direct trade. Sartorial beard unicorn lumbersexual kitsch dreamcatcher. Asymmetrical truffaut DIY, yes plz kogi 3 wolf moon twee neutral milk hotel next level.",
                               2: "Beard fingerstache organic, neutral milk hotel hot chicken DSA sustainable snackwave sus mustache squid crucifix jianbing shabby chic. Succulents pork belly solarpunk snackwave seitan la croix cred praxis church-key mumblecore sus. Vinyl Brooklyn banjo hot chicken beard lomo, narwhal ethical. Retro tonx etsy, next level kombucha microdosing ugh ennui.",
                               3: "Yes plz quinoa flexitarian distillery hot chicken blog ramps meggings schlitz praxis VHS lumbersexual craft beer. Shabby chic hashtag hammock neutra sriracha photo booth. Occupy vape plaid street art bespoke photo booth. Fanny pack forage prism, cornhole williamsburg irony sartorial mustache celiac venmo photo booth you probably haven't heard of them put a bird on it kogi praxis. ",       
                               4: "Pork belly cred YOLO, thundercats butcher yuccie cliche etsy pinterest copper mug bodega boys. Skateboard sus pickled, yuccie everyday carry marfa blackbird spyplane tofu neutra paleo cornhole irony tousled taxidermy vexillologist. Irony forage bitters copper mug. Tote bag ascot chillwave tacos master cleanse, chambray meggings vinyl tonx asymmetrical tofu banh mi tousled.",
                               5: "Coloring book gluten-free whatever, pok pok ascot truffaut mukbang man bun woke JOMO umami. Scenester squid twee VHS, air plant cornhole cliche tattooed irony aesthetic. Humblebrag echo park selfies hell of green juice, yes plz ennui DSA craft beer knausgaard flexitarian same selvage copper mug.",
                               6: "Pinterest cardigan kinfolk street art coloring book stumptown lomo gatekeep biodiesel bespoke hella paleo helvetica chillwave. Vape dreamcatcher tonx yes plz single-origin coffee. 3 wolf moon ennui pop-up yuccie cloud bread gluten-free, celiac sriracha jean shorts flexitarian crucifix la croix tumblr palo santo authentic. Grailed taxidermy letterpress tofu green juice freegan vegan mustache semiotics truffaut jawn cupping hexagon bitters actually.",
                               7: "Cray pop-up craft beer celiac. Viral artisan tumblr tousled green juice put a bird on it venmo. Vibecession before they sold out seitan pork belly, freegan fit asymmetrical. Chambray slow-carb polaroid, retro forage pabst farm-to-table keytar salvia grailed lo-fi. Man braid gastropub migas pop-up bespoke williamsburg. Gorpcore DIY kinfolk scenester letterpress tousled farm-to-table asymmetrical DSA cupping chia selvage cliche readymade.",
                               8: "I'm baby bodega boys fashion axe forage pop-up, fit succulents sriracha cornhole chicharrones master cleanse dreamcatcher tumblr subway tile. Cliche lumbersexual af, irony migas hot chicken literally vape tousled. Tacos photo booth la croix enamel pin woke meggings succulents mustache chambray distillery cupping pour-over. Paleo Brooklyn glossier drinking vinegar.",
                               9: "Twee poutine ramps, street art messenger bag air plant quinoa biodiesel literally occupy 90's tofu live-edge. DSA whatever iPhone prism. Meh cliche PBR&B 3 wolf moon Brooklyn kombucha edison bulb deep v. Pour-over fixie bushwick microdosing, listicle kombucha bodega boys selvage marfa palo santo. Cliche yes plz bicycle rights, church-key pork belly fanny pack jean shorts tote bag raw denim cray taxidermy pok pok.",
                               10: "Craft beer live-edge vexillologist, keffiyeh artisan farm-to-table vibecession venmo thundercats jawn vape post-ironic put a bird on it banh mi. Subway tile blackbird spyplane distillery, irony farm-to-table street art hammock hell of. Solarpunk chia hexagon mlkshk truffaut. Kinfolk messenger bag retro keffiyeh, umami lo-fi farm-to-table grailed mixtape gastropub butcher prism."
                               }
    
    def jgl_random_text(self) -> str:
        """Chooses a random string from possible text bank"""
        self.jgl_text = random.choice(self.possible_texts)
        return self.jgl_text.lower()