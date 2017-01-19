using UnityEngine;
using System.Collections;
using WebSocketSharp;

public class DataTrack : MonoBehaviour {

	public WebSocket ws_cur;
    GameObject drone;
    GameObject goal;
    Rigidbody droneRigidbody;
    private Vector3 droneCoords;
    private Vector3 droneVelocity;
    private Vector3 goalCoords;

    private Vector3 dir0;
    private Vector3 dir1;
    private Vector3 dir2;
    private Vector3 dir3;

    public int success = 0;

    private Movement droneMovement;

    private InstantiateGoal instantiateGoal;

	private CollisionDetect colDet;

    // Use this for initialization
    void Start () {
        dir0 = new Vector3(1f, 0f, 0f); //right
        dir1 = new Vector3(0f, 0f, 1f); //up
        dir2 = new Vector3(0f, 0f, -1f); // down
        dir3 = new Vector3(-1f, 0f, 0f); //left
        instantiateGoal = gameObject.GetComponent<InstantiateGoal>();
        drone = GameObject.FindGameObjectWithTag("Drone");
        droneMovement = drone.GetComponent<Movement>();
        droneRigidbody = drone.GetComponent<Rigidbody>();
        goal = null;
		ws_cur = new WebSocket ("ws://localhost:9001");
		ws_cur.OnMessage += (sender, e) => {
            if (e.IsText)
            {
                if (!droneMovement.netControlled)
                {
                    droneMovement.netControlled = true;
                }
                //Handles received action
                int action = int.Parse(e.Data.ToString());
                if (action == -1) {
                    if (goal != null)
                    {
						colDet.dest = true;
                    }
                }
                else if (action == 0) { droneMovement.direction = dir0; }
                else if (action == 1) { droneMovement.direction = dir1; }
                else if (action == 2) { droneMovement.direction = dir2; }
                else if (action == 3) { droneMovement.direction = dir3; }
				Debug.Log("Received action, " + e.Data.ToString());
				
            }
		};
		ws_cur.Connect ();
		ws_cur.Send ("unity");
	}
	
	// Update is called once per frame
	void Update () {
        if (gameObject.transform.childCount < 1)
        {
            goal = null;
			colDet = null;
        }
        if (gameObject.transform.childCount == 1 && goal == null)
        {
            goal = gameObject.transform.GetChild(0).gameObject;
			colDet = goal.GetComponent<CollisionDetect> ();
        }
	}

	string buildOutput() {
		string coord = round_dp (droneCoords.x).ToString () + ':' + round_dp (droneCoords.z).ToString ();
		string veloc = round_dp (droneVelocity.x).ToString () + ':' + round_dp (droneVelocity.z).ToString ();
		string goal = round_dp (goalCoords.x).ToString () + ':' + round_dp (goalCoords.z).ToString ();
        string succ = success.ToString();
		return coord + ':' + veloc + ':' + goal + ':' + succ;
	}

	float round_dp(float input){
		return Mathf.Round (input * 10f) / 10f;
	}

    public void SendData()
    {
        if (goal != null)
        {
            Debug.Log("Sending Data");
            goalCoords = goal.transform.position;
            droneCoords = drone.transform.position;
            droneVelocity = droneRigidbody.velocity;
            ws_cur.Send(buildOutput());
            if (success == 1)
            {
                success = 0;
            }
        }
    }
}
