using UnityEngine;
using System.Collections;

public class CollisionDetect : MonoBehaviour {

    private GameObject controller;

    private DataTrack dataScript;

	// Use this for initialization
	void Start () {
        controller = GameObject.FindGameObjectWithTag("Controller");
        dataScript = controller.GetComponent<DataTrack>();
	}
	
	// Update is called once per frame
	void Update () {
	    
	}
    void OnCollisionEnter(Collision other)
    {
        if(other.gameObject.tag == "Drone")
        {
            Destroy(gameObject);
            dataScript.success = 1;
        }
    }
}
