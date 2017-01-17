using UnityEngine;
using System.Collections;

public class Movement : MonoBehaviour {

    private Rigidbody droneRigidbody;
    public float forceMagnitude = 500000;

	// Use this for initialization
	void Start () {
        droneRigidbody = gameObject.GetComponent<Rigidbody>();
	}
	
	// Update is called once per frame
	void Update () {
        float inx = Input.GetAxis("Horizontal");
        float inz = Input.GetAxis("Vertical");
        float delta = Time.deltaTime;
        Vector3 direction = new Vector3(inx, 0, inz)*delta*forceMagnitude;
        droneRigidbody.AddForce(direction);
        transform.position = new Vector3(transform.position.x, 0.5f, transform.position.z);
        transform.eulerAngles = new Vector3(0f, transform.eulerAngles.y, 0f);
	}
}
