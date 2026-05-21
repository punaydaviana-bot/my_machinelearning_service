# ⚖️ CHAPTER 5: A/B Testing Phase

The true power of this setup is the ability to blindly test which model performs better in real-time. We registered Random Forest as `"production"` and Extra Trees as `"testing"`. 

## How A/B Testing Works

1. **Start the Test:** Send a POST request to `/api/v1/abtests`. You must provide a JSON payload that links Algorithm 1 (ID 1) with Algorithm 2 (ID 2).
2. **Routing Traffic:** Once the test begins, both models' statuses change to `"ab_testing"`. Whenever a user sends a request to `/api/v1/industry_classifier/predict?status=ab_testing`, Django intercepts it and randomly flips a coin to decide if Random Forest or Extra Trees computes the answer.
3. **Closing the Loop (Feedback):** Every prediction receives a `request_id`. Later, when the *actual* industry is known, you send a PUT request to `/api/v1/mlrequests/{id}` with `{"feedback": "Automotive"}`.
4. **Picking the Winner:** When you POST to `/api/v1/stop_ab_test/{id}`, Django calculates which algorithm had the highest accuracy based on the feedback. The winner is instantly promoted to `"production"`, and the loser demoted to `"testing"`.

## Next Steps for Production

Once you are satisfied with your model's performance on a local scale, refer to the **Docker Container** instructions in `Tutorial.md` (Chapter 7) to deploy this Django service globally via NGINX and Gunicorn.
