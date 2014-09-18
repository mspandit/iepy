from django.shortcuts import get_object_or_404, render_to_response, redirect

from corpus.models import Relation, TextSegment


def start_labeling_evidence(request, relation_id):
    relation = get_object_or_404(Relation, pk=relation_id)
    segment = relation.get_next_segment_to_label()
    if segment is None:
        return render_to_response('message.html',
                                  {'msg': 'There are no more evidence to label'})
    return redirect('corpus:label_evidence_for_segment', relation.pk, segment.pk)


def label_evidence_for_segment(request, relation_id, segment_id):
    segment = get_object_or_404(TextSegment, pk=segment_id)
    relation = get_object_or_404(Relation, pk=relation_id)
    segment.hydrate()
    return render_to_response(
        'label_evidence.html',
        {'title': 'hello world. You\'re gonna answer questions for segment '
         '"{0}" respect relation "{1}"'.format(segment, relation)})