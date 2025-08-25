Steps:

1 - python src/detection/click_detection_batch.py 

2 - python src/aggregation/aggregate_detections_batch.py reference_detections
  - python src/aggregation/aggregate_detections_batch.py model_detections 

3 - python src/aggregation/join_aggregated_files.py reference_detections
  - python src/aggregation/join_aggregated_files.py model_detections

4 - python src/visualization/plot_detection_comparison.py