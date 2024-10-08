package com.ozdemir.chatbot;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.NetworkResponse;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.HttpHeaderParser;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;

public class MainActivity extends AppCompatActivity
{
    private static final String TAG = "MainActivity";
    private ScrollView scrollView;
    private LinearLayout chatLayout;
    private EditText messageInput;
    private Button sendButton;
    private RequestQueue requestQueue;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        scrollView = findViewById(R.id.scrollView);
        chatLayout = findViewById(R.id.chatLayout);
        messageInput = findViewById(R.id.messageInput);
        sendButton = findViewById(R.id.sendButton);
        requestQueue = Volley.newRequestQueue(this);

        sendButton.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View v)
            {
                String message = messageInput.getText().toString();

                if (!message.isEmpty())
                {
                    addMessageToChat("You: " + message, true);
                    messageInput.setText("");
                    sendMessageToBot(message);
                }
            }
        });
    }

    private void addMessageToChat(String message, boolean isUser)
    {
        TextView textView = new TextView(this);
        textView.setText(message);
        textView.setTextColor(getResources().getColor(android.R.color.black)); // Mesaj rengini siyah yapıyoruz

        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams
        (
                LinearLayout.LayoutParams.WRAP_CONTENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
        );
        params.setMargins(0, 0, 0, 16); // Mesajlar arasında 16dp boşluk
        textView.setLayoutParams(params);

        if (isUser)
        {
            textView.setBackgroundResource(R.drawable.rounded_user_message);
        }

        else
        {
            textView.setBackgroundResource(R.drawable.rounded_bot_message);
        }
        chatLayout.addView(textView);

        scrollView.post(new Runnable()
        {
            @Override
            public void run() {
                scrollView.fullScroll(View.FOCUS_DOWN);
            }
        });
    }

    private void sendMessageToBot(String message)
    {
        String url = "LOCAL_IP_ADDRESS"; // IP adresinizi burada kullanın...
        JSONObject jsonBody = new JSONObject();

        try
        {
            jsonBody.put("sender", "user");
            jsonBody.put("message", message);
        }

        catch (JSONException e)
        {
            e.printStackTrace();
        }

        Log.d(TAG, "Sending message to bot: " + jsonBody.toString());

        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST, url, jsonBody, new Response.Listener<JSONObject>()
        {
            @Override
            public void onResponse(JSONObject response)
            {
                Log.d(TAG, "Received response from bot: " + response.toString());

                try
                {
                    JSONArray messages = response.getJSONArray("messages");

                    for (int i = 0; i < messages.length(); i++)
                    {
                        JSONObject botResponse = messages.getJSONObject(i);
                        String botMessage = botResponse.getString("text");
                        addMessageToChat("Bot: " + botMessage, false);
                    }
                }

                catch (JSONException e)
                {
                    e.printStackTrace();
                }
            }
        },
        new Response.ErrorListener()
        {
            @Override
            public void onErrorResponse(VolleyError error)
            {
                Log.e(TAG, "Error sending message to bot: " + error.toString());
                NetworkResponse networkResponse = error.networkResponse;

                if (networkResponse != null)
                {
                    String responseData;

                    try
                    {
                        responseData = new String(networkResponse.data, HttpHeaderParser.parseCharset(networkResponse.headers, "utf-8"));
                        Log.e(TAG, "Error response from bot: " + responseData);
                    }

                    catch (UnsupportedEncodingException e)
                    {
                        e.printStackTrace();
                    }
                }
            }
        })
        {
            @Override
            protected Response<JSONObject> parseNetworkResponse(NetworkResponse response)
            {
                try
                {
                    String jsonString = new String(response.data, HttpHeaderParser.parseCharset(response.headers, "utf-8"));
                    JSONArray jsonArray = new JSONArray(jsonString);
                    JSONObject jsonObject = new JSONObject();
                    jsonObject.put("messages", jsonArray);

                    return Response.success(jsonObject, HttpHeaderParser.parseCacheHeaders(response));
                }

                catch (UnsupportedEncodingException | JSONException e)
                {
                    return Response.error(new VolleyError(e));
                }
            }
        };
        requestQueue.add(jsonObjectRequest);
    }
}
