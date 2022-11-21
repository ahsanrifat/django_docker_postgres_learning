import json
import os
from random import randint

import django

from annotation import models

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'project.settings')
django.setup()


def produce_random_sentence():
    nouns = ["puppy", "car", "rabbit", "boy", "monkey",
             "man", "dog", "lady", "developer"]
    verbs = ["runs", "hits", "jumps", "drives", "barfs",
             "codes", "dances", "swims", "laughs", "roams",
             "talks", "moves"]
    adv = ["crazily.", "dutifully.", "foolishly.", "merrily.", "occasionally.",
           "unwillingly.", "eagerly.", "politely.", "randomly.", "with all energy.",
           "crazy fast.", "to death.", "so much better"]
    sentence = nouns[randint(0, len(nouns) - 1)] + " " + verbs[
        randint(0, len(verbs) - 1)] + " " + adv[randint(0, len(adv) - 1)] + " (" + str(randint(1, 1000000000)) + ")"
    return sentence


def produce_list_span(num_of_span):
    tags = ["PLACE", "TIME", "TITLE", "ORG", "DATE", "PERSON"]
    span_list = []
    for span_no in range(num_of_span):
        span_list.append(
            json.dumps(
                {
                    'char_start': span_no,
                    'char_end': randint(span_no + 1, 50),
                    'token_start': span_no,
                    'token_end': randint(span_no + 1, 50),
                    'label': tags[randint(0, len(tags) - 1)]
                }
            )
        )
    return span_list


def insert_dummy_data_in_database():
    annotator_combo_list = [
        [12, 13, 14, 15],
        [55, 34, 90, 45, 66],
        [266, 198, 340, 12],
        [56, 90, 88, 23, 277],
        [112, 124, 167, 198, 200],
        [225, 12, 13, 56],
        [18, 12, 145, 242, 198, 225]
    ]
    validator_id_list = [300, 307, 376, 391, 417, 419, 444, 300, 447]
    ner_data_count = models.Data.objects.all().count()
    print(f"NER Data Count---> {ner_data_count}")
    if ner_data_count < 10000000:
        print("Preparing Fake NER data to populate the DB----------")
        ner_data_list = []
        for project_id in range(1, 51):
            # ner data per project
            for ner_data_serial in range(randint(20, 70)):
                ner_text = produce_random_sentence()
                # randomly picking span number for each ner_data
                annotation_list = []
                validation = None
                num_of_span = randint(1, 4)
                # for every 5th project unassigned data will be inserted
                if project_id % 5 != 0:
                    group_id = randint(project_id * 10 - 9, project_id * 10)
                    data = models.Data(text=ner_text, project_id=project_id, group_id=group_id)
                    data.save()
                    print("=====Data=======>>>>", data)
                    group_annotator_list = annotator_combo_list[group_id % len(annotator_combo_list)]
                    group_validator = validator_id_list[group_id % len(validator_id_list)]
                    for annotator_id in group_annotator_list:
                        annotation = models.Annotation(
                            annotator_id=annotator_id,
                            data=data,
                            # making unannotated data for every 7th ner data
                            is_annotated=not (ner_data_serial % 7 == 0)
                        )
                        if annotation.is_annotated:
                            spans = produce_list_span(num_of_span)
                            annotation.span_lines = spans
                        annotation.save()
                    # every 7th data will not have any validation spans
                    validation = models.Validation(
                        validator_id=group_validator,
                        # making unvalidated data for every 7th ner data
                        data=data,
                        is_validated=not (ner_data_serial % 14 == 0),
                        is_rejected=False
                    )
                    if validation.is_validated:
                        validation.data.is_done = True
                        spans = produce_list_span(num_of_span)
                        validation.span_lines = spans
                    validation.save()
                else:
                    data = models.Data(text=ner_text, project_id=project_id)
                    data.save()
