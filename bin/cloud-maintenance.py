import argparse
import sys
from collections import namedtuple
from pathlib import Path

from axolpy import logging
from axolpy.aws import AWSRegion
from axolpy.cloudmaintenance import Operator, ResourceDataLoader
from axolpy.cloudmaintenance.steps import (DumpMysqlTableStatus, DumpPgstats,
                                           ModifyDatabaseClassType,
                                           ModifyDatabaseEngineVersion,
                                           QueryDatabaseStatus,
                                           QueryECSTaskStatus,
                                           QueryK8sDeploymentStatus,
                                           RestartECSService,
                                           RestartK8sDeployment,
                                           UpdateECSTaskCount,
                                           UpdateK8sDeploymentReplicas,
                                           UpdateK8sStatefulSetReplicas)

logging.load_config()
logger = logging.get_logger(name=Path(__file__).name)


def print_regions_detail(aws_regions: AWSRegion) -> None:
    """
    Print the resources in `aws_regions`.

    :param aws_regions: AWS Regions.
    :type aws_regions: :class:`AWSRegion`.
    """

    for region in aws_regions.values():
        logger.info(f"{region}")
        for db in region.rds_databases.values():
            logger.info(f"  {db}")
        for cluster in region.ecs_clusters.values():
            logger.info(f"  {cluster}")
            for service in cluster.services.values():
                logger.info(f"     {service}")
        for cluster in region.eks_clusters.values():
            logger.info(f"  {cluster}")
            for namespace in cluster.namespaces.values():
                logger.info(f"    {namespace}")
                for stateful_set in namespace.statefulsets.values():
                    logger.info(f"      {stateful_set}")
                for deployment in namespace.deployments.values():
                    logger.info(f"      {deployment}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data-path",
                        required=True,
                        help="The path to the data file.")
    parser.add_argument("-i", "--maintenance-id",
                        required=True,
                        help="Maintenance ID.")
    parser.add_argument("-o", "--operator",
                        required=True,
                        help="Name of operator.")
    args = parser.parse_args()

    data_path = Path(args.data_path)

    dist_path = Path("./dist", args.operator)
    dist_path.mkdir(parents=True, exist_ok=True)

    aws_regions = ResourceDataLoader.load_from_file(
        data_path=data_path,
        maintenance_id=args.maintenance_id
    )

    print_regions_detail(aws_regions=aws_regions)

    operator = Operator(id=args.operator)
    operator.data_loader.load_from_file(
        data_path=data_path,
        maintenance_id=args.maintenance_id,
        aws_regions=aws_regions)

    Step = namedtuple("Step", ["class_", "zeroinfy", "description"])
    steps = [Step(class_=UpdateECSTaskCount,
                  zeroinfy=True,
                  description="generate commands for updating ecs task count to 0"),
             Step(class_=UpdateK8sStatefulSetReplicas,
                  zeroinfy=True,
                  description="generate commands for updating k8s statefulset replicas to 0"),
             Step(class_=UpdateK8sDeploymentReplicas,
                  zeroinfy=True,
                  description="generate commands for updating k8s deployment replicas to 0"),
             Step(class_=DumpPgstats,
                  zeroinfy=False,
                  description="generate commands for dumping pgstats"),
             Step(class_=DumpMysqlTableStatus,
                  zeroinfy=False,
                  description="generate commands for dumping mysql table status"),
             Step(class_=ModifyDatabaseEngineVersion,
                  zeroinfy=False,
                  description="generate commands for modifying database engine version"),
             Step(class_=ModifyDatabaseClassType,
                  zeroinfy=False,
                  description="generate commands for modifying database class type"),
             Step(class_=QueryDatabaseStatus,
                  zeroinfy=False,
                  description="generate commands for querying database status"),
             Step(class_=DumpMysqlTableStatus,
                  zeroinfy=False,
                  description="generate commands for dumping mysql table status"),
             Step(class_=DumpPgstats,
                  zeroinfy=False,
                  description="generate commands for dumping pgstats"),
             Step(class_=RestartK8sDeployment,
                  zeroinfy=False,
                  description="generate commands for restarting k8s deployment"),
             Step(class_=RestartECSService,
                  zeroinfy=False,
                  description="generate commands for restarting ecs service"),
             Step(class_=RestartK8sDeployment,
                  zeroinfy=False,
                  description="generate commands for restarting eks deployment"),
             Step(class_=UpdateK8sDeploymentReplicas,
                  zeroinfy=False,
                  description="generate commands for updating k8s deployment replicas to resume"),
             Step(class_=UpdateK8sStatefulSetReplicas,
                  zeroinfy=False,
                  description="generate commands for updating k8s statefulset replicas to resume"),
             Step(class_=UpdateECSTaskCount,
                  zeroinfy=False,
                  description="generate commands for updating ecs task count to resume"),
             Step(class_=QueryK8sDeploymentStatus,
                  zeroinfy=False,
                  description="generate commands for querying k8s deployment status"),
             Step(class_=QueryECSTaskStatus,
                  zeroinfy=False,
                  description="generate commands for querying ecs task status")]

    step_no = 1
    for step in steps:
        logger.info(f"Step {step_no}: {step.description}")
        step_args = {"step_no": step_no,
                     "operator": operator,
                     "dist_path": dist_path}
        if step.zeroinfy:
            step_args["zeroinfy"] = True
        step_impl = step.class_(**step_args)
        step_impl.write_file()
        if step_impl.eligible():
            step_no += 1


if __name__ == "__main__":
    sys.exit(main())
