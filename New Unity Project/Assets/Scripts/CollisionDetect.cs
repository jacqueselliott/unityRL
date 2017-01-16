using UnityEngine;
using System.Collections;

public class CollisionDetect : MonoBehaviour {

	// Use this for initialization
	void Start () {
	    
	}
	
	// Update is called once per frame
	void Update () {
	    
	}
    void OnCollisionEnter(Collision other)
    {
        if(other.gameObject.tag == "Drone")
        {
            Destroy(gameObject);
        }
    }
}
