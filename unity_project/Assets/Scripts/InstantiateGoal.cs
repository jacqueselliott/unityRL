using UnityEngine;
using System.Collections;

public class InstantiateGoal : MonoBehaviour {

    public GameObject goal;
    private float planeSize = 10f;
    private GameObject drone;

	// Use this for initialization
	void Start () {
        drone = GameObject.FindGameObjectWithTag("Drone");
        CreateGoal();
	}
	
	// Update is called once per frame
	void Update () {
	    if (gameObject.transform.childCount == 0)
        {
            CreateGoal();
        }
	}

    void CreateGoal()
    {
        float randx = Random.Range(planeSize-1f, planeSize-1f);
        float randz = Random.Range(planeSize-1f, planeSize-1f);
        Vector3 spawnLocation = new Vector3(randx, 1f, randz);
        GameObject goalClone = (GameObject)Instantiate(goal, spawnLocation, Quaternion.identity);
        goalClone.transform.SetParent(gameObject.transform);
    }
}
