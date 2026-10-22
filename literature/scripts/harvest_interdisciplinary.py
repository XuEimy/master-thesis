#!/usr/bin/env python3
import harvest, concurrent.futures
harvest.QUERIES={
'semanticscholar':[
'"autobiographical memory" + ("self-memory" | "basic systems" | "encoding specificity" | "constructive episodic")',
'"autobiographical memory" + ("event boundary" | "event boundaries" | naturalistic | "context reinstatement")',
'"autobiographical memory" + (music | odor | odour | smell | multisensory | multimodal)',
'"autobiographical memory" + ("visual perspective" | "field perspective" | "observer perspective")',
'"narrative identity" + (autobiographical | memory)',
'"autobiographical reasoning" | "life story coherence"',
'"personal photography" + (memory | remembering | practice | everyday)',
'"digital photography" + (memory | remembering)',
'"photo elicitation" + (memory | remembering | autobiographical)',
'"sensory ethnography" + (memory | video | everyday)',
'"first-person documentary" | "autobiographical documentary"',
'"personal documentary" + (memory | autobiographical)',
'"home movies" + (memory | autobiographical)',
'"mediated memory" | "mediated memories"',
'"algorithmic memory" | "algorithmic memories"',
'"digital memory" + (autobiographical | personal | nostalgia | reminiscing)',
'"distributed cognition" + (autobiographical | remembering)',
'"extended mind" + (autobiographical | photographs | personal)',
'"autobiographical memory" + (objects | possessions | souvenirs)',
'"reminiscence" + (design | ritual | embodied | materiality)'
],
'europepmc':[
'TITLE_ABS:("generative AI" OR "generative artificial intelligence" OR "large language model") AND TITLE_ABS:("autobiographical memory" OR "episodic memory" OR reminiscence OR "false memories")',
'TITLE_ABS:("involuntary autobiographical") AND TITLE_ABS:(everyday OR cue OR cues)',
'TITLE_ABS:("autobiographical memory") AND TITLE_ABS:(narrative OR identity OR "self-memory")',
'TITLE_ABS:("autobiographical memory") AND TITLE_ABS:("event boundary" OR "event boundaries" OR naturalistic OR "context reinstatement")',
'TITLE_ABS:("autobiographical memory") AND TITLE_ABS:(music OR odor OR odour OR smell OR multisensory OR multimodal)',
'TITLE_ABS:("autobiographical memory") AND TITLE_ABS:("visual perspective" OR "field perspective" OR "observer perspective")'
]}
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(harvest.run,harvest.QUERIES))
