using UnityEngine;
using System.Collections;

public class InstantiateGoal : MonoBehaviour {

    public GameObject goal;
    private float planeSize;
    private GameObject drone;
    private bool discrete;
    private float discreteMagnitude;

	// Use this for initialization
	void Start () {
        drone = GameObject.FindGameObjectWithTag("Drone");
        planeSize = GameObject.Find("Ground").GetComponent<Collider>().bounds.size.x/2;
        discrete = drone.GetComponent<Movement>().discrete;
        discreteMagnitude = drone.GetComponent<Movement>().discreteMagnitude;
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
        Vector3 spawnLocation = drone.transform.position;
        //Keep trying new locations until one is sufficiently far from the drone
        //Play with this value to make the game slightly harder or easier
		while(Vector3.Distance(spawnLocation, drone.transform.position)<1.5f)
		{
            if (discrete)
            {
                spawnLocation = ChooseDiscreteLocation();
            }
            else
            {
                spawnLocation = ChooseContinuousLocation();
            }
		}
        Debug.Log(spawnLocation);
        GameObject goalClone = (GameObject)Instantiate(goal, spawnLocation, Quaternion.identity);
        goalClone.transform.SetParent(gameObject.transform);
    }

    private Vector3 ChooseDiscreteLocation()
    {
        int integerPlaneSize = (int)(planeSize/discreteMagnitude);
        int randx = Random.Range(-integerPlaneSize, integerPlaneSize);
        int randz = Random.Range(-integerPlaneSize, integerPlaneSize);
        return new Vector3(randx + (discreteMagnitude/2), 0.5f, randz + (discreteMagnitude / 2)) * discreteMagnitude;
    }

    private Vector3 ChooseContinuousLocation()
    {
        float randx = Random.Range(-planeSize + 1f, planeSize - 1f);
        float randz = Random.Range(-planeSize + 1f, planeSize - 1f);
        return new Vector3(randx, 0.5f, randz);
    }
}
